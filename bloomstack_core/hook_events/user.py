# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client, make_integration_request
from frappe.utils import cstr, get_host_name


def update_bloomtrace_user(user, method):
	if frappe.get_conf().developer_mode or frappe.get_conf().disable_user_sync:
		return

	if user.user_type == "System User" and user.name not in ["Administrator", "Guest"]:
		make_integration_request(user.doctype, user.name)


def execute_bloomtrace_integration_request():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	site_url = get_host_name()
	pending_requests = frappe.get_all("Integration Request",
		filters={
			"status": ["IN", ["Queued", "Failed"]],
			"reference_doctype": "User",
			"integration_request_service": "BloomTrace"
		},
		order_by="creation ASC",
		limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		user = frappe.get_doc("User", integration_request.reference_docname)
		try:
			bloomstack_site_user = insert_bloomstack_site_user(user, site_url, frappe_client)

			integration_request.error = ""
			integration_request.status = "Completed"
		except Exception as e:
			integration_request.error = cstr(e)
			integration_request.status = "Failed"

		integration_request.save(ignore_permissions=True)


def insert_bloomstack_site_user(user, site_url, frappe_client):
	bloomstack_site_user = make_bloomstack_site_user(user, site_url)
	return frappe_client.insert(bloomstack_site_user)

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