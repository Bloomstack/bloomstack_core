from __future__ import unicode_literals
from erpnext import get_default_company
import frappe
import re 
no_cache = 1


def get_context(context):
    token = frappe.local.request.args.get("token")
    docname = frappe.local.request.args.get("name")
    auth_req = frappe.get_doc("Authorization Request", docname)

    if not token or token != auth_req.token:
        context.error = "Token is not valid. Click here to re-send email"

    elif auth_req.status == "Approved":
        context.error = "This document has already been authorized by you!"
        
    elif auth_req.status == "Rejected":
        context.error = "This document has already been rejected by you!"

    frappe.local.flags.ignore_print_permissions = True
    print_doc = frappe.get_print(auth_req.linked_doctype, auth_req.linked_docname)
    context.print_doc = print_doc[print_doc.find('<body>')+len('<body>'):len(print_doc)-len('</body>')]
    context.doc = frappe.get_doc(auth_req.linked_doctype, auth_req.linked_docname)
    context.company = context.doc.company if hasattr(context.doc, 'company') else get_default_company()
    context.auth_req_docname = docname
