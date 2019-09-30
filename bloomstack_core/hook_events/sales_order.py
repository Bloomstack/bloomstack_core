import frappe
from erpnext import get_default_company
from frappe.utils import date_diff, now


def create_sales_invoice_against_contract():
	"""
		Daily scheduler event to create Sales Invoice against
		an active contract, based on the contract's payment terms
	"""

	sales_orders = frappe.get_all("Sales Order",
		filters={"docstatus": 1, "contract": ["not like", ""], "per_billed": ["<", 100]})

	for order in sales_orders:
		sales_order_doc = frappe.get_doc("Sales Order", order.name)

		for payment_term in sales_order_doc.payment_schedule:
			if payment_term.is_billed:
				continue

			if date_diff(payment_term.due_date, now()) > 15:
				continue

			sales_invoice = frappe.new_doc("Sales Invoice")
			sales_invoice.update({
				"customer": sales_order_doc.customer,
				"project": sales_order_doc.project,
				"items": [{
					"item_code": frappe.db.get_value("Contract", sales_order_doc.contract, "payment_item"),
					"qty": 1,
					"rate": payment_term.payment_amount,
					"amount": payment_term.payment_amount,
					"sales_order": order.name,
					"so_detail": sales_order_doc.items[0].name
				}]
			})
			sales_invoice.set_missing_values()
			sales_invoice.insert()
			frappe.db.set_value("Payment Schedule", payment_term.name, "is_billed", True)
