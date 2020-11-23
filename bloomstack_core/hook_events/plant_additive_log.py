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
		filters={"status": ["IN", ["Queued", "Failed"]], "reference_doctype": "Plant Additive log", "integration_request_service": "BloomTrace"},
		order_by="creation ASC",
		limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		plant_additive_log = frappe.get_doc("Plant Additive Log", integration_request.reference_docname)
		bloomtrace_plant_additive_log = frappe_client.get_doc("Plant Additive Log", integration_request.reference_docname)
		try:
			if not bloomtrace_plant_additive_log:
				insert_plant_additive_log(plant_additive_log, frappe_client)
			else:
				update_plant_additive_log(plant_additive_log, frappe_client)
			integration_request.error = ""
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)
		except Exception as e:
			integration_request.error = cstr(e)
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)

def insert_plant_additive_log(plant_additive_log, frappe_client):
	bloomtrace_plant_additive_log = make_plant_additive_log(plant_additive_log)
	frappe_client.insert(bloomtrace_plant_additive_log)

def update_plant_additive_log(plant_additive_log, frappe_client):
	bloomtrace_plant_additive_log = make_plant_additive_log(plant_additive_log)
	bloomtrace_plant_additive_log.update({
		"name": plant_additive_log.name
	})
	frappe_client.update(bloomtrace_plant_additive_log)

def make_plant_additive_log(plant_additive_log):
	site_url = frappe.utils.get_host_name()
	bloomtrace_plant_dict = {
		"doctype": "Plant Additive Log",
		"bloomstack_company": plant_additive_log.company,
		"additive":plant_additive_log.additive,
		"additive_type": plant_additive_log.additive_type,
		"total_amount_applied": plant_additive_log.total_amount_used,
		"application_device": plant_additive_log.application_device,
		"product_supplier": plant_additive_log.supplier,
		"total_amount_unit_of_measure": plant_additive_log.uom,
		"item": plant_additive_log.item,
		"location": plant_additive_log.location,
		"strain": plant_additive_log.strain,
		"plant_batch": plant_additive_log.plant_batch,
		"plant": plant_additive_log.plant,
		"actual_date": plant_additive_log.actual_date
	}
	return bloomtrace_plant_dict
