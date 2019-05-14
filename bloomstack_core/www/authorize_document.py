from __future__ import unicode_literals
import frappe

no_cache = 1

def get_context(context):
    token = frappe.local.request.args.get("token")
    docname = frappe.local.request.args.get("name")

    auth_req = frappe.get_doc("Authorization Request", docname)
    if not token or token == auth_req.token:
        context.error = "Token is not valid. Click here to re-send email"
        return

    if auth_req.status == "Approved":
        context.error = "You have already authorized this document"
        return

    frappe.local.flags.ignore_print_permissions = True
    context.print_doc = frappe.get_print(auth_req.linked_doctype, auth_req.linked_docname)
    context.auth_req_docname = docname