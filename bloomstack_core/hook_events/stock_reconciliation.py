# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import cstr, today
from bloomstack_core.bloomtrace import get_bloomtrace_client, make_integration_request


def create_integration_request(doc, method):
	for item in doc.items:
		if item.package_tag:
			make_integration_request("Stock Reconciliation", doc.name)
			break

def execute_bloomtrace_integration_request():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	pending_requests = frappe.get_all("Integration Request",
		filters={"status": ["IN", ["Queued", "Failed"]], "reference_doctype": "Stock Reconciliation", "integration_request_service": "BloomTrace"},
		order_by="creation ASC",
		limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		stock_reconciliation = frappe.get_doc("Stock Reconciliation", integration_request.reference_docname)
		bloomtrace_uid_transaction_log = frappe_client.get_doc("UID Transaction Log", integration_request.reference_docname)
		try:
			if not bloomtrace_uid_transaction_log:
				insert_uid_transaction_log(stock_reconciliation, frappe_client)
			else:
				update_uid_transaction_log(stock_reconciliation, frappe_client)
			integration_request.error = ""
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)
		except Exception as e:
			integration_request.error = cstr(frappe.get_traceback())
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)

def insert_uid_transaction_log(stock_reconciliation, frappe_client):
	bloomtrace_uid_transaction_log = make_uid_transaction_log(stock_reconciliation)
	frappe_client.insert(bloomtrace_uid_transaction_log)

def update_uid_transaction_log(stock_reconciliation, frappe_client):
	bloomtrace_uid_transaction_log = make_uid_transaction_log(stock_reconciliation)
	bloomtrace_uid_transaction_log.update({
		"name": stock_reconciliation.name
	})
	frappe_client.update(bloomtrace_uid_transaction_log)

def make_uid_transaction_log(stock_reconciliation):
	site_url = frappe.utils.get_host_name()
	bloomtrace_uid_transaction_log_dict = {
		"doctype": "UID Transaction Log",
		"client": site_url,
		"transaction_type": "Reconciliation",
		"transaction_date": today()
	}
	bloomtrace_uid_transaction_log_dict['items'] = [{
		"uid": stock_reconciliation.items[0].package_tag,
		"item": stock_reconciliation.items[0].item_code,
		"qty": stock_reconciliation.items[0].qty
	}]

	return bloomtrace_uid_transaction_log_dict