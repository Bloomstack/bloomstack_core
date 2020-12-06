import frappe
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
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
