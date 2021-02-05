import frappe

def execute():
	frappe.delete_doc_if_exists("Custom Field", "Job Applicant-resume_attachment-reqd")
	frappe.delete_doc_if_exists("Property Setter", "Job Applicant-resume_attachment-reqd")