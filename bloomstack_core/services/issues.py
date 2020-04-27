import frappe

@frappe.whitelist(allow_guest=True)
def issue_status_list():
	"""
	Returns an array of statuses available on the Issues doctype.
	"""
	meta = frappe.get_meta("Issue")
	return meta.get_options("status").split("\n")
