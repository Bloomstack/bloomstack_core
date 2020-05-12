import frappe
from frappe.modules.utils import sync_customizations


def execute():
	sync_customizations("bloomstack_core")

	doctypes = ["Quotation", "Sales Order", "Sales Invoice", "Delivery Note"]

	for doctype in doctypes:
		frappe.db.sql("""
			UPDATE
				`tab{doctype}`
			SET
				order_type = new_order_type
		""".format(doctype=doctype))
