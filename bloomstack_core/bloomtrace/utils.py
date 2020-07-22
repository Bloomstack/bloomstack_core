import frappe
from frappe.frappeclient import FrappeClient, AuthError


def get_bloomtrace_client():
	url = frappe.conf.get("bloomtrace_server")
	username = frappe.conf.get("bloomtrace_username")
	password = frappe.conf.get("bloomtrace_password")

	if not url:
		return

	try:
		client = FrappeClient(url, username=username, password=password, verify=True)
	except ConnectionError:
		return
	except AuthError:
		return

	return client


def make_integration_request(doctype, docname):
	if frappe.get_conf().enable_bloomtrace or doctype=="User":
		integration_request = frappe.new_doc("Integration Request")
		integration_request.update({
			"integration_type": "Remote",
			"integration_request_service": "BloomTrace",
			"status": "Queued",
			"reference_doctype": doctype,
			"reference_docname": docname
		})
		integration_request.save(ignore_permissions=True)
