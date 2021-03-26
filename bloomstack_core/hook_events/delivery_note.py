# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloom Stack and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import cstr, get_host_name
from bloomstack_core.bloomtrace import get_bloomtrace_client


def link_invoice_against_delivery_note(delivery_note, method):
	for item in delivery_note.items:
		if item.against_sales_order and not item.against_sales_invoice:
			sales_invoice_details = frappe.get_all("Sales Invoice Item",
				filters={"docstatus": 1, "sales_order": item.against_sales_order},
				fields=["distinct(parent)", "delivery_note"])

			if sales_invoice_details and len(sales_invoice_details) == 1:
				if sales_invoice_details[0].delivery_note:
					continue
				frappe.db.set_value("Delivery Note Item", item.name,
				    "against_sales_invoice", sales_invoice_details[0].parent)

def execute_bloomtrace_integration_request():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	pending_requests = frappe.get_all("Integration Request",
		filters={
			"status": ["IN", ["Queued", "Failed"]],
			"reference_doctype": "Delivery Note",
			"integration_request_service": "BloomTrace"
		},
		order_by="creation ASC",
		limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		delivery_note = frappe.get_doc("Delivery Note", integration_request.reference_docname)

		try:
			if not delivery_note.is_return:
				insert_delivery_payload(delivery_note, frappe_client)

			if delivery_note.lr_no or (delivery_note.estimated_arrival and delivery_note.departure_time):
				# If delivery trip is created or estimated_arrival and departure_time is present, only then move forward to integrate with BloomTrace
				insert_transfer_template(delivery_note, frappe_client)

			integration_request.error = ""
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)
		except Exception as e:
			integration_request.error = cstr(frappe.get_traceback())
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)


def insert_transfer_template(delivery_note, frappe_client):
	estimated_arrival = delivery_note.estimated_arrival
	departure_time = delivery_note.departure_time

	if delivery_note.lr_no:
		delivery_trip = frappe.get_doc("Delivery Trip", delivery_note.lr_no)
		for stop in delivery_trip.delivery_stops:
			if stop.delivery_note == delivery_note.name:
				estimated_arrival = stop.estimated_arrival

		if not estimated_arrival:
			try:
				delivery_trip.process_route(False)
			except Exception:
				frappe.throw(_("Estimated Arrival Times are not present."))

		if not departure_time:
			departure_time = delivery_trip.departure_time

	transfer_template_packages = []
	for item in delivery_note.items:
		if item.package_tag:
			transfer_template_packages.append({
				"package_tag": item.package_tag,
				"wholesale_price": item.amount
			})

	site_url = get_host_name()
	transfer_template = {
		"doctype": "Transfer Template",
		"bloomstack_company": delivery_note.company,
		"delivery_note": delivery_note.name,
		"transporter_facility_license": frappe.db.get_value("Company", delivery_note.company, "license"),
		"transporter_phone": frappe.db.get_value("Company", delivery_note.company, "phone_no"),
		"recipient_license_number": delivery_note.license,
		"vechile_make": frappe.db.get_value("Vehicle", delivery_note.vehicle_no, "make"),
		"vehicle_model": frappe.db.get_value("Vehicle", delivery_note.vehicle_no, "model"),
		"vehicle_license_plate_number": delivery_note.vehicle_no,
		"driver_name": delivery_note.driver_name,
		"driver_license_number": frappe.db.get_value("Driver", delivery_note.driver, "license_number"),
		"estimated_departure": departure_time,
		"estimated_arrival": estimated_arrival,
		"packages": transfer_template_packages
	}
	frappe_client.insert(transfer_template)

def insert_delivery_payload(delivery_note, frappe_client):
	"""
	Create the request body for package doctype in bloomtrace from a Delivery Note.

	Args:
		delivery_note (object): The `Delivery Note` Frappe object.

	Returns:
		payload (list of dict): The `Delivery Note` payload, if an Item is moved / created, otherwise `None` is reported to BloomTrace
	"""

	for item in delivery_note.items:
		payload = {}
		package_ingredients = []

		if item.package_tag:
			source_package_tag = frappe.db.get_value("Package Tag", item.package_tag, "source_package_tag")
			if source_package_tag:
				package_ingredients.append({
					"package": source_package_tag,
					"quantity": item.qty,
					"unit_of_measure": item.uom,
				})
			elif item.warehouse:
				payload = {
					"tag": item.package_tag,
					"item": item.item_name,
					"quantity": item.qty,
					"unit_of_measure": item.uom,
					"patient_license_number": "",
					"actual_date": delivery_note.lr_date or delivery_note.posting_date
				}

		if not payload:
			return

		payload["doctype"] = "Package"
		payload["Ingredients"] = package_ingredients
		payload["bloomstack_company"] = delivery_note.company

		frappe_client.insert(payload)
