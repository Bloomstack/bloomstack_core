import frappe
from bloomstack_core.bloomtrace import make_integration_request

def create_integration_request(doc, method):
	if method == "validate":
		if not doc.is_new():
			make_integration_request(doc.doctype, doc.name)
	elif method == "after_insert":
		make_integration_request(doc.doctype, doc.name)
