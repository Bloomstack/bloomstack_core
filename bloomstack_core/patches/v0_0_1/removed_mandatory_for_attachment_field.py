import frappe

def execute():
	frappe.delete_doc_if_exists("Custom Field", "Job Applicant-resume_attachment-reqd")