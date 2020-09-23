import frappe
from frappe import _
from frappe.frappeclient import FrappeClient, AuthError


def get_bloomtrace_client():
	url = frappe.conf.bloomtrace_server
	username = frappe.conf.bloomtrace_username
	password = frappe.conf.bloomtrace_password

	if not (url and username and password):
		return

	try:
		client = FrappeClient(url, username=username, password=password, verify=True)
	except ConnectionError:
		return
	except AuthError:
		return

	return client


def make_integration_request(doctype, docname):

	if frappe.conf.enable_bloomtrace or doctype == "User":
		request = frappe.get_doc({
			"doctype": "Integration Request",
			"integration_type": "Remote",
			"integration_request_service": "BloomTrace",
			"status": "Queued",
			"reference_doctype": doctype,
			"reference_docname": docname
		}).insert(ignore_permissions=True)
