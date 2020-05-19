import frappe
from frappe.modules.utils import sync_customizations

def execute():

	frappe.reload_doc('selling', 'doctype', 'customer', force=True)
	frappe.reload_doc('setup', 'doctype', 'company', force=True)
	frappe.reload_doc('buying', 'doctype', 'supplier', force=True)
	sync_customizations("bloomstack_core")

	customers = frappe.get_all("Customer", fields=["*"])
	suppliers = frappe.get_all("Supplier", fields=["*"])
	companies = frappe.get_all("Company", fields=["*"])

	entities = customers
	entities.extend(suppliers)
	entities.extend(companies)

	for entity in entities:
		if entity.license:
			default_license = {
				"license": entity.license,
				"is_default": 1
			}
			entity.set("licenses", default_license)
			entity.save()