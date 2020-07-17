import json

import frappe
from erpnext.selling.doctype.sales_order.sales_order import create_pick_list, make_sales_invoice
from erpnext.stock.doctype.batch.batch import get_batch_qty
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
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


def check_overdue_status(sales_order, method):
	overdue_conditions = [
		sales_order.docstatus == 1,
		sales_order.status not in ["On Hold", "Closed", "Completed"],
		sales_order.skip_delivery_note == 0,
		flt(sales_order.per_delivered, 6) < 100,
		getdate(sales_order.delivery_date) < getdate(today()),
	]

	is_overdue = all(overdue_conditions)
	sales_order.db_set("is_overdue", is_overdue)


def update_order_status():
	"""
		Daily scheduler to check if a Sales Order has become overdue
	"""

	frappe.db.sql("""
		UPDATE
			`tabSales Order`
		SET
			is_overdue = 1
		WHERE
			docstatus = 1
				AND delivery_date < CURDATE()
				AND status NOT IN ("On Hold", "Closed", "Completed")
				AND skip_delivery_note = 0
				AND per_delivered < 100
	""")

def validate_delivery_date(self):
	if self.order_type == 'Sales' and not self.skip_delivery_note:
		delivery_date_list = [d.delivery_date for d in self.get("items") if d.delivery_date]
		if self.delivery_date:
			for d in self.get("items"):
				if not d.delivery_date:
					d.delivery_date = self.delivery_date
				if getdate(self.transaction_date) > getdate(d.delivery_date):
					frappe.msgprint(_("Expected Delivery Date should be after Sales Order Date"),
						indicator='orange', title=_('Warning'))
		else:
			frappe.throw(_("Please enter Delivery Date"))

	self.validate_sales_mntc_quotation()

SalesOrder.validate_delivery_date = validate_delivery_date