from __future__ import unicode_literals

import re

import frappe
from erpnext import get_default_company

no_cache = 1


def get_context(context):
	token = frappe.local.request.args.get('token')
	docname = frappe.local.request.args.get("name")
	auth_req = frappe.get_doc("Authorization Request", docname)

	if not token or token != auth_req.token:
		context.error = "Invalid token. You cannot authorize this document."
	elif auth_req.status == "Approved":
		context.error = "This document has already been authorized"
	elif auth_req.status == "Rejected":
		context.error = "This document has already been unauthorized"

	frappe.local.flags.ignore_print_permissions = True
	print_doc = frappe.get_print(auth_req.linked_doctype, auth_req.linked_docname)

	context.print_doc = print_doc[print_doc.find('<body>') + len('<body>'):len(print_doc) - len('</body>')]
	context.doc = frappe.get_doc(auth_req.linked_doctype, auth_req.linked_docname)
	context.company = context.doc.company if hasattr(context.doc, 'company') else get_default_company()
	context.auth_req_docname = docname
	context.authorizer_email = auth_req.authorizer_email
	context.status = auth_req.status

	print_format = "Bloomstack Contract" if auth_req.linked_doctype == 'Contract' else "Standard"
	context.print_url = "/{0}/{1}?format={2}&key={3}&trigger_print=1".format(auth_req.linked_doctype, auth_req.linked_docname, print_format, context.doc.get_signature())

@frappe.whitelist(allow_guest = True)
def custom_print_doc(auth_req_docname):
	frappe.local.flags.ignore_print_permissions = True

	auth_req = frappe.get_doc("Authorization Request", auth_req_docname)
	print_format = "Bloomstack Contract" if auth_req.linked_doctype == 'Contract' else "Standard"
	print_doc = frappe.get_print(auth_req.linked_doctype, auth_req.linked_docname, print_format)
	custom_print_format = print_doc[print_doc.find('<body>') + len('<body>'):len(print_doc) - len('</body>')]

	return custom_print_format
