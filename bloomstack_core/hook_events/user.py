# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import get_url, cstr
from urllib.parse import urlparse

def set_works_with_bloomstack_false(user, method):
	user.works_with_bloomstack=False

def validate_if_bloomstack_user(user, method):
	if user.works_with_bloomstack and not user.enabled:
		frappe.throw("Please contact support to disable Bloomstack Users.")

def update_bloomtrace_user(user, method):
	if frappe.get_conf().enable_bloomtrace and not user.is_new():
		if user.user_type == "System User" and user.name not in ["Administrator", "Guest"] and not user.works_with_bloomstack:
			integration_request = frappe.new_doc("Integration Request")
			integration_request.update({
				"integration_type": "Remote",
				"integration_request_service": "BloomTrace",
				"status": "Queued",
				"reference_doctype": "User",
				"reference_docname": user.name
			})
			integration_request.save(ignore_permissions=True)

def execute_bloomtrace_integration_request():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
			return

	site_url = urlparse(get_url()).netloc
	pending_requests = frappe.get_all("Integration Request", 
		filters={"status": ["IN", ["Queued", "Failed"]], "reference_doctype": "User", "integration_request_service": "BloomTrace"},
		order_by="creation ASC", limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		user = frappe.get_doc("User", integration_request.reference_docname)
		try:
			bloomstack_site_user = frappe_client.get_doc("Bloomstack Site User", filters={
					"bloomstack_site": site_url, 
					"email": user.email
				})
			if not bloomstack_site_user:
				bloomstack_site_user = insert_bloomstack_site_user(user, site_url, frappe_client)
			else:
				doc_name = bloomstack_site_user[0].get('name')
				bloomstack_site_user = update_bloomstack_site_user(user, doc_name, site_url, frappe_client)	
			frappe.db.set_value("User", user.name, "works_with_bloomstack", bloomstack_site_user.get('works_with_bloomstack'))
			integration_request.error = ""
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)	
		except Exception as e:
			integration_request.error = cstr(e)
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)

def insert_bloomstack_site_user(user, site_url, frappe_client):
	bloomstack_site_user = make_bloomstack_site_user(user, site_url)
	return frappe_client.insert(bloomstack_site_user)

def update_bloomstack_site_user(user, doc_name, site_url, frappe_client):
	bloomstack_site_user = make_bloomstack_site_user(user, site_url)
	bloomstack_site_user.update({
		"name": doc_name
	})
	return frappe_client.update(bloomstack_site_user)

def make_bloomstack_site_user(user, site_url):
	bloomstack_site_user = {
		"doctype": "Bloomstack Site User",
		"enabled": user.enabled,
		"first_name": user.first_name,
		"last_name": user.last_name,
		"email": user.email,
		"bloomstack_site": site_url
	}
	return bloomstack_site_user