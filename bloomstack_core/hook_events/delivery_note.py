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
			insert_transfer_template(delivery_note, frappe_client)
			integration_request.error = ""
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)
		except Exception as e:
			integration_request.error = cstr(e)
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)


def insert_transfer_template(delivery_note, frappe_client):
	delivery_trip = frappe.get_doc("Delivery Trip", delivery_note.lr_no)
	estimated_arrival = ''
	for stop in delivery_trip.delivery_stops:
		if stop.delivery_note == delivery_note.name:
			estimated_arrival = stop.estimated_arrival

	transfer_template_packages = []
	for item in delivery_note.items:
		if item.package_tag:
			transfer_template_packages.append({
				"package_tag": item.package_tag,
				"wholesale_price": item.rate
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
		"estimated_departure": delivery_trip.departure_time,
		"estimated_arrival": estimated_arrival,
		"packages": transfer_template_packages
	}
	frappe_client.insert(transfer_template)
