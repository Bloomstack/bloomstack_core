# -*- coding: utf-8 -*-
# Copyright (c) 2021, Bloomstack Inc. and contributors
# For license information, please see license.txt

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


def make_integration_request(doctype, docname, integration):
	settings = frappe.get_cached_doc("Compliance Settings")
	if not (frappe.conf.enable_bloomtrace and settings.is_compliance_enabled) or \
		frappe.db.exists("Integration Request", {"reference_doctype": doctype, "reference_docname": docname}):
		return

	doc = frappe.get_doc(doctype, docname)
	company = settings.get("company", {"company": doc.company}) and settings.get("company", {"company": doc.company})[0]
	fieldname = "push_{0}".format(frappe.scrub(integration))

	if not company or not company.get(fieldname):
		return

	integration_request = frappe.get_doc({
		"doctype": "Integration Request",
		"integration_type": "Remote",
		"integration_request_service": "BloomTrace",
		"status": "Queued",
		"reference_doctype": doctype,
		"reference_docname": docname,
		"endpoint": integration
	}).save(ignore_permissions=True)


def create_integration_request(doc, method):
	make_integration_request(doc.doctype, doc.name)
