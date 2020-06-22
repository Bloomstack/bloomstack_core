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
	if sales_invoice.is_return:
		return

	metrc_payload = map_metrc_payload(sales_invoice)

	if metrc_payload:
		metrc = get_metrc()

		if not metrc:
			return

		response = metrc.sales.receipts.post(json = metrc_payload)
		log_request(response.url, metrc_payload, response, "Sales Invoice", sales_invoice.name)

		if not response.ok:
			frappe.throw(_(response.raise_for_status()))

def map_metrc_payload(sales_invoice):
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

	if len(transactions) == 0:
		return False

	return [{
		"SalesDateTime": frappe.utils.now(),
		"SalesCustomerType": "Consumer",
		"Transactions": transactions
	}]
