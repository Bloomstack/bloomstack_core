import frappe

def execute():
	frappe.delete_doc_if_exists("Custom Field", "User-column_break_2")
	frappe.delete_doc_if_exists("Custom Field", "User-works_with_bloomstack")

	frappe.db.sql("DELETE FROM `tabActivity Log` where user='Administrator'")
	frappe.db.sql("DELETE FROM `tabIntegration Request` where reference_doctype='User'")