import frappe


def set_issue_as_replied(communication, method):
	if communication.reference_doctype == "Issue":
		if communication.sent_or_received == "Sent":
			frappe.db.set_value("Issue", communication.reference_name, "status", "Pending Response")
		elif communication.sent_or_received == "Received":
			frappe.db.set_value("Issue", communication.reference_name, "status", "Open")
