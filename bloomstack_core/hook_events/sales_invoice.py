# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloom Stack and contributors
# For license information, please see license.txt

import json

import frappe
from bloomstack_core.compliance.utils import get_metrc
from frappe import _
from frappe.utils import now


def create_metrc_sales_receipt(sales_invoice, method):
	if sales_invoice.is_return:
		return

	metrc = get_metrc()
	if not metrc:
		return

	payload = get_metrc_payload(sales_invoice)
	if not payload:
		return

	response = metrc.sales.receipts.post(json=payload)

	integration_request = frappe.new_doc("Integration Request")
	integration_request.update({
		"integration_type": "Remote",
		"integration_request_service": "Metrc",
		"reference_doctype": sales_invoice.doctype,
		"reference_docname": sales_invoice.name
	})

	if not response.ok:
		integration_request.status = "Failed"
		integration_request.error = json.dumps(json.loads(response.text), indent=4, sort_keys=True)
		integration_request.save(ignore_permissions=True)
		frappe.db.commit()

		if isinstance(response.json(), list):
			for error in response.json():
				frappe.throw(_(error.get("message")))
		elif isinstance(response.json(), dict):
			frappe.throw(_(response.json().get("Message")))
	else:
		integration_request.status = "Completed"
		integration_request.save(ignore_permissions=True)


def get_metrc_payload(sales_invoice):
	settings = frappe.get_single("Compliance Settings")

	if not settings.is_compliance_enabled:
		return

	transactions = []
	for item in sales_invoice.items:
		if item.package_tag:
			transactions.append({
				"PackageLabel": item.package_tag,
				"Quantity": item.qty,
				"UnitOfMeasure": "Grams",
				"TotalAmount": item.amount
			})

	if not transactions:
		return

	return [{
		"SalesDateTime": now(),
		"SalesCustomerType": "Consumer",
		"Transactions": transactions
	}]
