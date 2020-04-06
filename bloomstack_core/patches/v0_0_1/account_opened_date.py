import frappe
from frappe.modules.utils import sync_customizations


def execute():
	sync_customizations("bloomstack_core")
	leads = frappe.get_all("Lead", fields=["name", "creation"])

	for lead in leads:
		result = frappe.db.get_value("Customer", {"lead_name": lead.name}, ["creation","opening_date"], as_dict=True)
		if result.opening_date:
			frappe.db.set_value("Lead", lead.name, "account_opened_date", result.opening_date)
		else:
			frappe.db.set_value("Lead", lead.name, "account_opened_date", result.creation)

