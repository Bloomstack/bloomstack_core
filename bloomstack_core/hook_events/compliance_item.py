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

	site_url = urlparse(get_url()).netloc
	pending_requests = frappe.get_all("Integration Request",
		filters={"status": ["IN", ["Queued", "Failed"]], "reference_doctype": "Compliance Item", "integration_request_service": "BloomTrace"},
		order_by="creation ASC", limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		compliance_item = frappe.get_doc("Compliance Item", integration_request.reference_docname)
		try:
			if not compliance_item.bloomtrace_id:
				insert_compliance_item(compliance_item, site_url, frappe_client)
			else:
				update_compliance_item(compliance_item, site_url, frappe_client)
			integration_request.error = ""
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)
		except Exception as e:
			integration_request.error = cstr(e)
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)


def insert_compliance_item(compliance_item, site_url, frappe_client):
	bloomtrace_compliance_item_dict = make_compliance_item(compliance_item, site_url)
	bloomtrace_compliance_item = frappe_client.insert(bloomtrace_compliance_item_dict)
	bloomtrace_id = bloomtrace_compliance_item.get('name')
	frappe.db.set_value("Compliance Item", compliance_item.name, "bloomtrace_id", bloomtrace_id)


def update_compliance_item(compliance_item, site_url, frappe_client):
	bloomtrace_compliance_item_dict = make_compliance_item(compliance_item, site_url)
	bloomtrace_compliance_item_dict.update({
		"name": compliance_item.bloomtrace_id
	})
	frappe_client.update(bloomtrace_compliance_item_dict)


def make_compliance_item(compliance_item, site_url):
	bloomtrace_compliance_item_dict = {
		"doctype": "Compliance Item",
		"bloomstack_site": site_url,
		"item_code": compliance_item.item_code,
		"item_name": compliance_item.item_name,
		"enable_metrc": compliance_item.enable_metrc,
		"metrc_id": compliance_item.metrc_id,
		"metrc_item_category": compliance_item.metrc_item_category,
		"metrc_unit_value": compliance_item.metrc_unit_value,
		"metrc_uom": compliance_item.metrc_uom,
		"metrc_unit_uom": compliance_item.metrc_unit_uom
	}
	return bloomtrace_compliance_item_dict
