# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import cstr

def execute_bloomtrace_integration_request():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
			return

	pending_requests = frappe.get_all("Integration Request",
		filters={"status": ["IN", ["Queued", "Failed"]], "reference_doctype": "Package Tag", "integration_request_service": "BloomTrace"},
		order_by="creation ASC", limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		package_tag = frappe.get_doc("Package Tag", integration_request.reference_docname)
		uid = frappe_client.get_doc("UID", integration_request.reference_docname)
		try:
			if not uid:
				insert_uid(package_tag, frappe_client)
			else:
				update_uid(package_tag, frappe_client)
			integration_request.error = ""
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)
		except Exception as e:
			integration_request.error = cstr(e)
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)

def insert_uid(package_tag, frappe_client):
	uid = make_uid(package_tag)
	frappe_client.insert(uid)

def update_uid(package_tag, frappe_client):
	uid = make_uid(package_tag)
	uid.update({
		"name": package_tag.name
	})
	frappe_client.update(uid)
 
def make_uid(package_tag):
	item = frappe.db.get_value("Compliance Item", package_tag.item_code, "bloomtrace_id")
	manufacturing_date = frappe.db.get_value("Batch", package_tag.batch_no, "manufacturing_date") if package_tag.batch_no else None
	expiry_date = frappe.db.get_value("Batch", package_tag.batch_no, "expiry_date") if package_tag.batch_no else None

	uid = {
		"doctype": "UID",
		"item": item,
		"uid_type": "Package",
		"uid_number": package_tag.name,
		"batch_number": package_tag.batch_no,
		"manufacturing_date": manufacturing_date,
		"expiry_date": expiry_date
	}
	return uid