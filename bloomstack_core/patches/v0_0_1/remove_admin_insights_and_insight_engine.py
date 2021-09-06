import frappe

def execute():
	for page in ["admin_insights", "insight-engine"]:
		frappe.delete_doc_if_exists("Page", page)
