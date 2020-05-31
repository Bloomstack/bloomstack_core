# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe

def update_bloomtrace_user(user, method):
	if frappe.get_conf().enable_bloomtrace:
		if user.user_type == "System User" and user.name not in ["Administrator", "Guest"] and not user.from_bloomstack:
			integration_request = frappe.new_doc("Integration Request")
			integration_request.update({
				"integration_type": "Remote",
				"integration_request_service": "BloomTrace",
				"status": "Queued",
				"reference_doctype": "User",
				"reference_docname": user.name
			})
			integration_request.save(ignore_permissions=True)
