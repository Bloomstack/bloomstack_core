# Copyright (c) 2013, Neil Lasrado and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import flt, global_date_format


def execute(filters=None):
	filters = filters or {}

	columns = get_columns(filters)
	data = get_collections(filters.get("date_range"), filters.get("driver"), filters.get("show_individual_stops"))

	return columns, data


def get_collections(date_range, driver, show_individual_stops=False):
	data = []

	filters = {
		"departure_time": ["between", date_range],
		"docstatus": 1
	}
	if driver:
		filters["driver"] = driver

	delivery_trips = frappe.get_all("Delivery Trip", filters=filters)

	for trip in delivery_trips:
		delivery_trip = frappe.get_doc("Delivery Trip", trip.name)

		sales_invoices = []
		delivery_amount = tax_amount = promotional_amount = unprocessed_amount = processed_amount = paid_amount = returned_amount = cancelled_amount = 0.0

		for stop in delivery_trip.delivery_stops:
			if stop.delivery_note:
				# Base amounts
				discount_stop_amount = promotional_stop_amount = 0.0
				is_promotional_delivery = frappe.db.get_value("Delivery Note", stop.delivery_note, "order_type") == "Promotional"

				if stop.grand_total == 0:
					discount_stop_amount = frappe.db.get_value("Delivery Note", stop.delivery_note, "discount_amount")

				if is_promotional_delivery:
					promotional_stop_amount = discount_stop_amount

				# TODO: Replace promotional amount with full discount, and breakdown each
				# 		discount as a separate column, if D9 wants to
				delivery_stop_amount = stop.grand_total + promotional_stop_amount

				amount_under_terms = get_amount_under_terms(stop.sales_invoice)
				tax_stop_amount = get_tax_amount(stop.sales_invoice) if stop.sales_invoice else 0.0

				# Paid amounts
				unprocessed_stop_amount = get_paid_amount(stop.sales_invoice, stop.delivery_note, docstatus=0)
				processed_stop_amount = get_paid_amount(stop.sales_invoice, stop.delivery_note, docstatus=1)
				paid_stop_amount = unprocessed_stop_amount + processed_stop_amount

				# Returned amounts
				returned_stop_amount = abs(frappe.db.get_value("Delivery Note",
					{"docstatus": 1, "return_against": stop.delivery_note, "issue_credit_note": 0},
					"sum(grand_total)") or 0)
				cancelled_stop_amount = abs(frappe.db.get_value("Delivery Note",
					{"docstatus": 1, "return_against": stop.delivery_note, "issue_credit_note": 1},
					"sum(grand_total)") or 0)

				if driver or show_individual_stops:
					# Append individual driver collections
					data.append({
						"driver": delivery_trip.driver_name,
						"delivery_trip": trip.name,
						"delivery_date": global_date_format(delivery_trip.departure_time),
						"sales_invoices": stop.sales_invoice,
						"customer": stop.customer,
						"total_amount": delivery_stop_amount,
						"tax_amount": tax_stop_amount,
						"promotional_amount": promotional_stop_amount,
						"amount_under_terms": amount_under_terms,
						"cancelled_amount": cancelled_stop_amount,
						"expected_amount": stop.grand_total - amount_under_terms - cancelled_stop_amount,
						"returned_amount": returned_stop_amount,
						"payment_received": unprocessed_stop_amount,
						"payment_processed": processed_stop_amount,
						"total_payment": paid_stop_amount
					})
				else:
					delivery_amount += delivery_stop_amount
					tax_amount += tax_stop_amount
					promotional_amount += promotional_stop_amount
					returned_amount += returned_stop_amount
					cancelled_amount += cancelled_stop_amount
					unprocessed_amount += unprocessed_stop_amount
					processed_amount += processed_stop_amount
					paid_amount += paid_stop_amount

			if stop.sales_invoice:
				sales_invoices.append(stop.sales_invoice)

		if not driver and not show_individual_stops:
			# Append cumulative collections for each Trip
			amount_under_terms = get_amount_under_terms(sales_invoices)
			sales_invoices = ", ".join(sales_invoices)

			data.append({
				"driver": delivery_trip.driver_name,
				"delivery_trip": trip.name,
				"delivery_date": global_date_format(delivery_trip.departure_time),
				"sales_invoices": sales_invoices,
				"total_amount": delivery_amount,
				"tax_amount": tax_amount,
				"promotional_amount": promotional_amount,
				"amount_under_terms": amount_under_terms,
				"cancelled_amount": cancelled_amount,
				"expected_amount": delivery_trip.package_total - amount_under_terms - cancelled_amount,
				"returned_amount": returned_amount,
				"payment_received": unprocessed_amount,
				"payment_processed": processed_amount,
				"total_payment": paid_amount
			})

	return data


def get_amount_under_terms(invoice):
	amount_under_terms = 0.0

	if not invoice:
		return amount_under_terms

	if isinstance(invoice, list):
		for inv in invoice:
			payment_terms_template, outstanding_amount = frappe.db.get_value(
				"Sales Invoice", inv, ["payment_terms_template", "outstanding_amount"])

			if payment_terms_template:
				amount_under_terms += outstanding_amount
	else:
		payment_terms_template, outstanding_amount = frappe.db.get_value(
			"Sales Invoice", invoice, ["payment_terms_template", "outstanding_amount"])

		if payment_terms_template:
			amount_under_terms = outstanding_amount

	return amount_under_terms


def get_tax_amount(invoice):
	tax_accounts = [account.name for account in frappe.get_all("Account", filters={"account_type": "Tax"})]

	tax_amounts = frappe.get_all("Sales Taxes and Charges",
		filters={"parent": invoice, "account_head": ["IN", tax_accounts]},
		fields=["tax_amount"])

	tax_amount = sum([tax.tax_amount for tax in tax_amounts if tax.tax_amount])

	return tax_amount


def get_paid_amount(sales_invoice, delivery_note, docstatus):
	paid_amount = 0.0
	invoices = []

	if sales_invoice:
		invoices = [sales_invoice]
	elif delivery_note:
		dn_items = frappe.get_all("Delivery Note Item",
			filters={"parent": delivery_note},
			fields=["distinct(against_sales_invoice)"])

		invoices = [item.against_sales_invoice for item in dn_items if item.against_sales_invoice]

	for invoice in invoices:
		payments = frappe.get_all("Payment Entry Reference",
			filters={"reference_name": invoice, "docstatus": docstatus},
			fields=["distinct(parent)"])

		for payment in payments:
			paid_amount += frappe.db.get_value("Payment Entry", payment.parent, "paid_amount") or 0.0

	return paid_amount


def get_columns(filters):
	columns = [
		{
			"label": _("Driver"),
			"fieldname": "driver",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Delivery Trip"),
			"fieldname": "delivery_trip",
			"fieldtype": "Link",
			"options": "Delivery Trip",
			"width": 120
		},
		{
			"label": _("Delivery Date"),
			"fieldname": "delivery_date",
			"fieldtype": "Data",
			"width": 130
		},
		{
			"label": _("Sales Invoice(s)"),
			"fieldname": "sales_invoices",
			"fieldtype": "Link" if filters.get("show_individual_stops") else "Data",
			"options": "Sales Invoice" if filters.get("show_individual_stops") else "",
			"width": 150 if filters.get("show_individual_stops") else 200
		}
	]

	if filters.get("driver") or filters.get("show_individual_stops"):
		columns.extend([
			{
				"label": _("Customer"),
				"fieldname": "customer",
				"fieldtype": "Link",
				"options": "Customer",
				"width": 200
			}
		])

	columns.extend([
		{
			"label": _("Total Delivery Value (A)"),
			"fieldname": "total_amount",
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"label": _("Taxes Due"),
			"fieldname": "tax_amount",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Promotions (B)"),
			"fieldname": "promotional_amount",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Amount under Terms (C)"),
			"fieldname": "amount_under_terms",
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"label": _("Cancelled Amount (D)"),
			"fieldname": "cancelled_amount",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Expected Amount (A - B - C - D)"),
			"fieldname": "expected_amount",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Returned Amount"),
			"fieldname": "returned_amount",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Payment Received (X)"),
			"fieldname": "payment_received",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Payment Processed (Y)"),
			"fieldname": "payment_processed",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Total Payment (X + Y)"),
			"fieldname": "total_payment",
			"fieldtype": "Currency",
			"width": 100
		}
	])

	return columns