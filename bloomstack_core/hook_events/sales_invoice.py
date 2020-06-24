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


def create_metrc_sales_receipt(sales_invoice, methods):
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
		"reference_doctype": "Sales Invoice",
		"reference_docname": sales_invoice.name
	})

	if not response.ok:
		integration_request.status = "Failed"
		integration_request.error = response.text
		frappe.throw(_(response.raise_for_status()))
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
		"SalesDateTime": frappe.utils.now(),
		"SalesCustomerType": "Consumer",
		"Transactions": transactions
	}]
