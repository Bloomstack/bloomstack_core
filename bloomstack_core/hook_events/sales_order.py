import json

import frappe
from erpnext.selling.doctype.sales_order.sales_order import create_pick_list, make_sales_invoice


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
		customer = frappe.db.get_value("Sales Order", order, "customer")

		pick_lists = frappe.get_all("Pick List",
			filters=[
				["Pick List Item", "sales_order", "=", order]
			],
			fields=["parent"],
			distinct=True)
		pick_lists = [item.parent for item in pick_lists if item.parent]

		if not pick_lists:
			order_doc = create_pick_list(order)
			order_doc.save()
			pick_lists = [order_doc.name]

		created_orders.append({
			"sales_order": order,
			"customer": customer,
			"pick_lists": pick_lists
		})

	return created_orders
