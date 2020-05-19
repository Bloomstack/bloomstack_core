import frappe
from frappe.modules.utils import sync_customizations


def execute():
	frappe.reload_doc('bloomstack_core', 'doctype', 'compliance_license_detail', force=True)
	frappe.reload_doc('selling', 'doctype', 'customer', force=True)
	frappe.reload_doc('setup', 'doctype', 'company', force=True)
	frappe.reload_doc('buying', 'doctype', 'supplier', force=True)
	sync_customizations("bloomstack_core")

	customers = frappe.get_all("Customer", fields=["*"])
	suppliers = frappe.get_all("Supplier", fields=["*"])
	entities = customers + suppliers

	for entity in entities:
		if entity.license:
			entity.append("licenses", {
				"license": entity.license,
				"is_default": 1
			})
			entity.save()
