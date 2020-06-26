import frappe
from frappe.modules.utils import sync_customizations


def execute():
	sync_customizations("bloomstack_core")

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
