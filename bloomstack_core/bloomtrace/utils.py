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
	if frappe.conf.enable_bloomtrace and frappe.db.get_single_value("Compliance Settings", "is_compliance_enabled"):
		settings = frappe.get_cached_doc("Compliance Settings")
		companies = [company.company for company in settings.company]
		doc = frappe.get_doc(doctype, docname)

		if not doc.company in companies:
			return

		if not frappe.db.exists("Integration Request", {"reference_doctype": doctype, "reference_docname": docname}):
			integration_request = frappe.get_doc({
				"doctype": "Integration Request",
				"integration_type": "Remote",
				"integration_request_service": "BloomTrace",
				"status": "Queued",
				"reference_doctype": doctype,
				"reference_docname": docname
			}).save(ignore_permissions=True)


def create_integration_request(doc, method):
	make_integration_request(doc.doctype, doc.name)
