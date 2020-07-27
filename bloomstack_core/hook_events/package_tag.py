# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import get_url, cstr
from urllib.parse import urlparse

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
		bloomtrace_package_tag = frappe_client.get_doc("Package Tag", integration_request.reference_docname)
		try:
			if not bloomtrace_package_tag:
				insert_pakage_tag(package_tag, frappe_client)
			else:
				update_pakage_tag(package_tag, frappe_client)
			integration_request.error = ""
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)
		except Exception as e:
			integration_request.error = cstr(e)
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)

def insert_pakage_tag(package_tag, frappe_client):
	bloomtrace_package_tag = make_pakage_tag(package_tag)
	frappe_client.insert(bloomtrace_package_tag)

def update_pakage_tag(package_tag, frappe_client):
	bloomtrace_package_tag = make_pakage_tag(package_tag)
	bloomtrace_package_tag.update({
		"name": package_tag.name
	})
	frappe_client.update(bloomtrace_package_tag)

def make_pakage_tag(package_tag):
	site_url = urlparse(get_url()).netloc
	item = frappe.db.get_value("Compliance Item", package_tag.item_code, "bloomtrace_id")
	manufacturing_date = frappe.db.get_value("Batch", package_tag.batch_no, "manufacturing_date") if package_tag.batch_no else None
	expiry_date = frappe.db.get_value("Batch", package_tag.batch_no, "expiry_date") if package_tag.batch_no else None

	bloomtrace_package_tag = {
		"doctype": "Package Tag",
		"bloomstack_site": site_url,
		"item": item,
		"uid_number": package_tag.name,
		"batch_number": package_tag.batch_no,
		"manufacturing_date": manufacturing_date,
		"expiry_date": expiry_date
	}
	return bloomtrace_package_tag