# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from bloomstack_core.utils import get_metrc, log_request
from datetime import datetime


def set_invoice_status(sales_invoice, method):
	sales_invoice.set_status()
	sales_invoice.set_indicator()

def create_sales_receipt(sales_invoice, methods):
	if sales_invoice.get("is_return"):
		return

	metrc_payload = map_metrc_payload(sales_invoice)

	if metrc_payload:
		metrc = get_metrc()

		if not metrc:
			return

		response = metrc.sales.receipts.post(json = metrc_payload)

		integration_request = frappe.new_doc("Integration Request")
		integration_request.update({
			"integration_type": "Remote",
			"integration_request_service": "Metrc",
			"reference_doctype": "Sales Invoice",
			"reference_docname": sales_invoice.get("name")
		})

		if not response.ok:
			integration_request.status = "Failed"
			integration_request.error = response.text
			frappe.throw(_(response.raise_for_status()))

		integration_request.status = "Completed"
		integration_request.save(ignore_permissions=True)

def map_metrc_payload(sales_invoice):
	settings = frappe.get_single("Compliance Settings")

	if not settings.is_compliance_enabled:
		return

	transactions = []

	for item in sales_invoice.get("items"):
		if item.get("package_tag"):
			transactions.append({
				"PackageLabel": item.get("package_tag"),
				"Quantity": item.get("qty"),
				"UnitOfMeasure": "Grams",
				"TotalAmount": item.get("amount")
			})

	if len(transactions) == 0:
		return False

	return [{
		"SalesDateTime": frappe.utils.now(),
		"SalesCustomerType": "Consumer",
		"Transactions": transactions
	}]
