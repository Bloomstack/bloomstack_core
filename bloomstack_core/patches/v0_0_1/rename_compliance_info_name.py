import frappe
from frappe.modules.utils import sync_customizations

def execute():
	frappe.reload_doc('bloomstack_core', 'doctype', 'compliance_info', force=True)
	compliance_info_list = frappe.get_all("Compliance Info", fields=["name", "license_number"])
	
	for compliance_info in compliance_info_list:
		if compliance_info.name != compliance_info.license_number:
			frappe.rename_doc("Compliance Info", compliance_info.name, compliance_info.license_number)
