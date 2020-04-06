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


	customers = frappe.get_all("Customer", fields=["opening_date", "lead_name"])

	for customer in customers:
		if customer.lead_name:
			doc = frappe.get_doc("Lead", customer.lead_name)
			doc.account_opening_date = customer.opening_date
			doc.save()