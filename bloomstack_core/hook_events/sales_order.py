import json

import frappe
from erpnext.selling.doctype.sales_order.sales_order import create_pick_list, make_sales_invoice
from erpnext.stock.doctype.batch.batch import get_batch_qty
from frappe import _
from frappe.utils import flt


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
				batches = get_available_batches(warehouse, item.item_code)
				frappe.throw(_("""
					Row #{0}: The batch {1} has only {2} qty. Either select a different
					batch that has more than {3} qty available, or split the row to sell
					from multiple batches.<br><br>
					Available batches with qty:<br><li>{4}</li>
				""").format(item.idx, item.batch_no, batch_qty, qty, batches))


def get_available_batches(warehouse, item_code):
	batches = get_batch_qty(warehouse=warehouse, item_code=item_code)

	batch_dict = {item.get('batch_no'): "{0} {1}".format(item.qty, item.stock_uom) for item in batches}
	value = '<br><li>'.join(' = '.join((key, val)) for (key, val) in batch_dict.items())
	return value
