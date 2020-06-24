# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import json

import frappe
from bloomstack_core.utils import get_metrc
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
from frappe import _
from frappe.utils import get_link_to_form


def link_invoice_against_delivery_note(delivery_note, method):
	for item in delivery_note.items:
		if item.against_sales_order and not item.against_sales_invoice:
			sales_invoice = frappe.get_all("Sales Invoice Item",
				filters={"docstatus": 1, "sales_order": item.against_sales_order},
				fields=["distinct(parent)"])

			if sales_invoice and len(sales_invoice) == 1:
				item.against_sales_invoice = sales_invoice[0].parent


def create_metrc_transfer_template(delivery_note, method):
	if delivery_note.is_return:
		return

	metrc = get_metrc()
	if not metrc:
		return

	payload = map_metrc_payload(delivery_note)
	if not payload:
		return

	response = metrc.transfers.templates.post(json=payload)

	integration_request = frappe.new_doc("Integration Request")
	integration_request.update({
		"integration_type": "Remote",
		"integration_request_service": "Metrc",
		"reference_doctype": "Delivery Note",
		"reference_docname": delivery_note.name
	})

	if not response.ok:
		integration_request.status = "Failed"
		integration_request.error = json.dumps(json.loads(response.text), indent=4, sort_keys=True)
		integration_request.save(ignore_permissions=True)
		frappe.db.commit()

		for error in response.json():
			frappe.throw(_(error.get("message")))
	else:
		integration_request.status = "Completed"
		integration_request.save(ignore_permissions=True)


def map_metrc_payload(delivery_note):
	settings = frappe.get_single("Compliance Settings")

	if not settings.is_compliance_enabled:
		return

	packages = []
	for item in delivery_note.items:
		if item.package_tag:
			packages.append({
				"PackageLabel": item.package_tag
			})

	if not packages:
		return

	return [{
		"Name": delivery_note.name,
		"TransporterFacilityLicenseNumber": settings.metrc_license_no,
		"EstimatedDepartureDateTime": frappe.utils.now(),
		"EstimatedArrivalDateTime": frappe.utils.now(),
		"Destinations": [
			{
				"RecipientLicenseNumber": settings.metrc_license_no,
				"TransferTypeName": "Transfer",
				"EstimatedDepartureDateTime": frappe.utils.now(),
				"EstimatedArrivalDateTime": frappe.utils.now(),
				"Packages": packages
			}
		]
	}]


def make_sales_invoice_for_delivery(delivery_note, method):
	if not frappe.db.get_single_value("Accounts Settings", "auto_create_invoice_on_delivery_note_submit"):
		return

	# If the delivery is already billed, don't create a Sales Invoice
	if delivery_note.per_billed == 100:
		return

	# Picking up sales orders for 2 reasons:
	# 1. A Delivery Note can be made against multiple orders, so they all need to be invoiced
	# 2. Using the `make_sales_invoice` in `delivery_note.py` doesn't consider already invoiced orders
	sales_orders = [item.against_sales_order for item in delivery_note.items if item.against_sales_order]
	sales_orders = list(set(sales_orders))

	new_invoices = []
	for order in sales_orders:
		invoice = make_sales_invoice(order)

		if len(invoice.items) > 0:
			invoice.set_posting_time = True
			invoice.posting_date = delivery_note.posting_date
			invoice.posting_time = delivery_note.posting_time

			invoice.save()
			invoice.submit()

			new_invoices.append(get_link_to_form("Sales Invoice", invoice.name))

	if new_invoices:
		new_invoices = ", ".join(str(invoice) for invoice in new_invoices)
		frappe.msgprint(_("The following Sales Invoice(s) were automatically created: {0}".format(new_invoices)))
