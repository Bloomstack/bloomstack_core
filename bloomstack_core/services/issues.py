import frappe

@frappe.whitelist(allow_guest=True)
def issueStatusList():
	"""
	Returns an array of statuses available on the Issues doctype.
	"""
	meta = frappe.get_meta("Issue")
	return meta.get_options("status").split("\n")
