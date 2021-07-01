import frappe

def execute():
	frappe.delete_doc_if_exists("Custom Field", "Work Order-title")
