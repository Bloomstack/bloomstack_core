# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloom Stack and contributors
# For license information, please see license.txt

import json

import frappe
from erpnext.selling.doctype.sales_order.sales_order import create_pick_list, make_sales_invoice, make_delivery_note
from erpnext.stock.doctype.batch.batch import get_batch_qty
from frappe import _
from frappe.utils import flt, getdate, today


def create_sales_invoice_against_contract():
	"""
		Daily scheduler event to create Sales Invoice against
		an active contract, based on the contract's payment terms
	"""

	sales_orders = frappe.get_all("Sales Order",
		filters={"docstatus": 1, "contract": ["not like", ""], "per_billed": ["<", 100]})

	for order in sales_orders:
		sales_invoice = make_sales_invoice(order.name)
		sales_invoice.save()


@frappe.whitelist()
def create_multiple_pick_lists(orders):
	orders = json.loads(orders)

	created_orders = []
	for order in orders:
		created = False
		customer = frappe.db.get_value("Sales Order", order, "customer")

		# check if a Pick List already exists against the order
		pick_lists = frappe.get_all("Pick List",
			filters=[
				["Pick List", "docstatus", "<", 2],
				["Pick List Item", "sales_order", "=", order]
			],
			distinct=True)
		pick_lists = [item.name for item in pick_lists if item.name]

		# if none are found, then create a new Pick List
		if not pick_lists:
			order_doc = create_pick_list(order)

			# if no items can be picked, do not create an empty Pick List
			if order_doc.get("locations"):
				order_doc.save()
				pick_lists = [order_doc.name]
				created = True
			else:
				pick_lists = []

		created_orders.append({
			"sales_order": order,
			"customer": customer,
			"pick_lists": pick_lists,
			"created": created
		})

	return created_orders

@frappe.whitelist()
def create_multiple_sales_invoices(orders):
	orders = json.loads(orders)

	created_orders = []
	for order in orders:
		created = False
		customer = frappe.db.get_value("Sales Order", order, "customer")

		# check if a Sales Invoice already exists against the order
		sales_invoices = frappe.get_all("Sales Invoice",
			filters=[
				["Sales Invoice", "docstatus", "<", 2],
				["Sales Invoice Item", "sales_order", "=", order]
			],
			distinct=True)
		sales_invoices = [item.name for item in sales_invoices if item.name]

		# if none are found, then create a new Sales Invoice
		if not sales_invoices:
			order_doc = make_sales_invoice(order)

			# if no items can be avilable, do not create an empty Sales Invoice
			if order_doc.get("items"):
				order_doc.save()
				sales_invoices = [order_doc.name]
				created = True
			else:
				sales_invoices = []

		created_orders.append({
			"sales_order": order,
			"customer": customer,
			"sales_invoices": sales_invoices,
			"created": created
		})

	return created_orders

@frappe.whitelist()
def create_muliple_delivery_notes(orders):
	orders = json.loads(orders)

	created_orders = []
	for order in orders:
		created = False
		customer = frappe.db.get_value("Sales Order", order, "customer")

		# check if a Delivery Note already exists against the order
		delivery_notes = frappe.get_all("Delivery Note",
			filters=[
				["Delivery Note", "docstatus", "<", 2],
				["Delivery Note Item", "against_sales_order", "=", order]
			],
			distinct=True)
		delivery_notes = [item.name for item in delivery_notes if item.name]

		# if none are found, then create a new Pick List
		if not delivery_notes:
			order_doc = make_delivery_note(order)

			# if no items can be picked, do not create an empty Pick List
			if order_doc.get("items"):
				order_doc.save()
				delivery_notes = [order_doc.name]
				created = True
			else:
				delivery_notes = []

		created_orders.append({
			"sales_order": order,
			"customer": customer,
			"delivery_notes": delivery_notes,
			"created": created
		})

	return created_orders


def validate_batch_item(sales_order, method):
	for item in sales_order.items:
		qty = item.stock_qty or item.transfer_qty or item.qty or 0
		has_batch_no = frappe.db.get_value('Item', item.item_code, 'has_batch_no')
		warehouse = item.warehouse

		if has_batch_no and warehouse and qty > 0:
			if not item.batch_no:
				return

			batch_qty = get_batch_qty(batch_no=item.batch_no, warehouse=warehouse)
			if flt(batch_qty, item.precision("qty")) < flt(qty, item.precision("qty")):
				frappe.throw(_("""
					Row #{0}: The batch {1} has only {2} qty. Either select a different
					batch that has more than {3} qty available, or split the row to sell
					from multiple batches.
				""").format(item.idx, item.batch_no, batch_qty, qty))


def check_overdue_status(sales_order, method=None):
	overdue_conditions = [
		sales_order.docstatus == 1,
		sales_order.status not in ["On Hold", "Closed", "Completed"],
		sales_order.skip_delivery_note == 0,
		flt(sales_order.per_delivered, 6) < 100,
		getdate(sales_order.delivery_date) < getdate(today()),
	]

	is_overdue = all(overdue_conditions)
	if is_overdue != sales_order.is_overdue:
		sales_order.db_set("is_overdue", is_overdue)


def update_order_status():
	"""
		Daily scheduler to check if a Sales Order has become overdue
	"""

	orders = frappe.get_all("Sales Order", filters={"docstatus": 1})

	for order in orders:
		check_overdue_status(frappe.get_doc("Sales Order", order))
