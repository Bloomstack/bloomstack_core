import frappe
from frappe.modules.utils import sync_customizations


def execute():
	sync_customizations("bloomstack_core")
	leads = frappe.get_all("Lead", fields=["name", "creation"])

	for lead in leads:
		creation = frappe.db.get_value("Customer", {"lead_name": lead.name}, "creation")
		if creation:
			frappe.db.set_value("Lead", lead.name, "account_opened_date", creation)
