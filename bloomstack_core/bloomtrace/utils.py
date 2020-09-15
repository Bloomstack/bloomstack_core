import frappe
from frappe import _
from frappe.frappeclient import FrappeClient, AuthError


def get_bloomtrace_client():
	url = frappe.conf.get("bloomtrace_server")
	username = frappe.conf.get("bloomtrace_username")
	password = frappe.conf.get("bloomtrace_password")

	if not (url and username and password):
		return

	try:
		client = FrappeClient(url, username=username, password=password, verify=True)
	except ConnectionError:
		frappe.throw(_("Could not connect to Bloomtrace."))
	except AuthError:
		frappe.throw(_("Authentication error while connecting to Bloomtrace."))

	return client


def make_integration_request(doctype, docname):

	if frappe.conf.get("enable_bloomtrace") or doctype == "User":
		frappe.get_doc({
			"doctype": "Integration Request",
			"integration_type": "Remote",
			"integration_request_service": "BloomTrace",
			"status": "Queued",
			"reference_doctype": doctype,
			"reference_docname": docname
		}).insert(ignore_permissions=True)
