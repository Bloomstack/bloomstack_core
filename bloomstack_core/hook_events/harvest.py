# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import cstr, get_url
from bloomstack_core.bloomtrace import get_bloomtrace_client


def create_integration_request(doc, method):
	integration_request = frappe.new_doc("Integration Request")
	integration_request.update({
		"integration_type": "Remote",
		"integration_request_service": "BloomTrace",
		"method": "POST",
		"status": "Queued",
		"reference_doctype": doc.doctype,
		"reference_docname": doc.name
	})
	integration_request.save(ignore_permissions=True)

def execute_bloomtrace_integration_request():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	pending_requests = frappe.get_all("Integration Request",
		filters={"status": ["IN", ["Queued", "Failed"]], "reference_doctype": "Harvest", "integration_request_service": "BloomTrace"},
		order_by="creation ASC",
		limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		harvest = frappe.get_doc("Harvest", integration_request.reference_docname)
		bloomtrace_harvest = frappe_client.get_doc("Harvest", filters={"harvest" : integration_request.reference_docname})
		try:
			if not bloomtrace_harvest:
				insert_harvest(harvest, frappe_client)
			else:
				update_harvest(harvest, frappe_client)
			integration_request.error = ""
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)
		except Exception as e:
			integration_request.error = cstr(e)
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)

def insert_harvest(harvest, frappe_client):
	bloomtrace_harvest = make_harvest(harvest)
	frappe_client.insert(bloomtrace_harvest)

def update_harvest(harvest, frappe_client):
	print("-----------------------------------------------", harvest.as_dict())
	bloomtrace_harvest = make_harvest(harvest)
	print("==========================================", bloomtrace_harvest)
	bloomtrace_harvest.update({
		"name": harvest.name
	})
	frappe_client.update(bloomtrace_harvest)

def make_harvest(harvest):
	# site_url = frappe.utils.get_host_name()
	site_url = "http://bloomstack_demo:8000"
	bloomtrace_harvest_dict = {
		"doctype": "Harvest",
		"bloomstack_site": site_url,
		"harvest":harvest.name,
		"harvest_type": harvest.harvest_type,
		"harvest_location":harvest.harvest_location,
		"drying_location": harvest.drying_location,
		"current_weight": harvest.harvest_weight,
		"unit_of_weight_name": harvest.harvest_uom,
		"is_finished": harvest.is_finished
	}
	return bloomtrace_harvest_dict
