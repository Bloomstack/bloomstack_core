import frappe
from frappe.modules.utils import sync_customizations

def execute():
	frappe.reload_doc('bloomstack_core', 'doctype', 'license', force=True)
	compliance_info_list = frappe.get_all("License", fields=["name", "license_number"])
	
	for compliance_info in compliance_info_list:
		if compliance_info.name != compliance_info.license_number:
			frappe.rename_doc("License", compliance_info.name, compliance_info.license_number)
