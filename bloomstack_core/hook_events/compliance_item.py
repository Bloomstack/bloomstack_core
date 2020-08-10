# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

from urllib.parse import urlparse

import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from bloomstack_core.compliance.item import create_item, update_item
from frappe import _
from frappe.utils import cstr, get_url


def sync_metrc_item(compliance_item, method):
	if compliance_item.enable_metrc:
		if method == "validate":
			if not compliance_item.is_new():
				_sync_metrc_item(compliance_item)
		elif method == "after_insert":
			_sync_metrc_item(compliance_item)


def _sync_metrc_item(compliance_item):
	item = frappe.get_doc("Item", compliance_item.item_code)

	# Merge Item and Compliance Item data
	item.update(compliance_item.as_dict())

	if not compliance_item.metrc_id:
		metrc_id = create_item(item)

		if metrc_id:
			frappe.db.set_value("Compliance Item", compliance_item.name, "metrc_id", metrc_id)
			frappe.msgprint(_("{} was successfully created in METRC (ID number: {}).".format(item.item_name, metrc_id)))
		else:
			frappe.msgprint(_("{} was successfully created in METRC.".format(item.item_name)))
	else:
		update_item(item)
		frappe.msgprint(_("{} was successfully updated in METRC.".format(item.item_name)))


def execute_bloomtrace_integration_request():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
			return

	pending_requests = frappe.get_all("Integration Request",
		filters={"status": ["IN", ["Queued", "Failed"]], "reference_doctype": "Compliance Item", "integration_request_service": "BloomTrace"},
		order_by="creation ASC", limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		compliance_item = frappe.get_doc("Compliance Item", integration_request.reference_docname)
		try:
			if not compliance_item.bloomtrace_id:
				insert_compliance_item(compliance_item, frappe_client)
			else:
				update_compliance_item(compliance_item, frappe_client)
			integration_request.error = ""
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)
		except Exception as e:
			integration_request.error = cstr(e)
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)


def insert_compliance_item(compliance_item, frappe_client):
	bloomtrace_compliance_item_dict = make_compliance_item(compliance_item)
	bloomtrace_compliance_item = frappe_client.insert(bloomtrace_compliance_item_dict)
	bloomtrace_id = bloomtrace_compliance_item.get('name')
	frappe.db.set_value("Compliance Item", compliance_item.name, "bloomtrace_id", bloomtrace_id)


def update_compliance_item(compliance_item, frappe_client):
	bloomtrace_compliance_item_dict = make_compliance_item(compliance_item)
	bloomtrace_compliance_item_dict.update({
		"name": compliance_item.bloomtrace_id
	})
	frappe_client.update(bloomtrace_compliance_item_dict)


def make_compliance_item(compliance_item):
	site_url = urlparse(get_url()).netloc
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
