# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

from urllib.parse import urlparse
import frappe
from frappe.utils import cstr, get_url
from bloomstack_core.bloomtrace import get_bloomtrace_client, make_integration_request

def create_integration_request(doc, method):
	make_integration_request(doc.doctype, doc.name, "Plant Batch")

def execute_bloomtrace_integration_request():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	pending_requests = frappe.get_all("Integration Request",
		filters={"status": ["IN", ["Queued", "Failed"]], "reference_doctype": "Plant Batch", "integration_request_service": "BloomTrace"},
		order_by="creation ASC",
		limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		plant_batch = frappe.get_doc("Plant Batch", integration_request.reference_docname)
		bloomtrace_plant_batch = frappe_client.get_doc("Plant Batch", integration_request.reference_docname)
		try:
			if not bloomtrace_plant_batch:
				insert_plant_batch(plant_batch, frappe_client)
			else:
				update_plant_batch(plant_batch, frappe_client)
			integration_request.error = ""
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)
		except Exception as e:
			integration_request.error = cstr(frappe.get_traceback())
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)

def insert_plant_batch(plant_batch, frappe_client):
	bloomtrace_plant_batch = make_plant_batch(plant_batch)
	frappe_client.insert(bloomtrace_plant_batch)

def update_plant_batch(plant_batch, frappe_client):
	bloomtrace_plant_batch = make_plant_batch(plant_batch)
	bloomtrace_plant_batch.update({
		"name": plant_batch.name
	})
	frappe_client.update(bloomtrace_plant_batch)

def make_plant_batch(plant_batch):
	bloomtrace_plant_batch_dict = {
		"doctype": "Plant Batch",
		"bloomstack_company": plant_batch.company,
		"plant_batch":plant_batch.title,
		"type": plant_batch.cycle_type,
		"strain_name": plant_batch.strain,
		"location_name": plant_batch.location,
		"planted_date": plant_batch.start_date,
		"growth_date": plant_batch.growth_date,
		"untracked_count": plant_batch.untracked_count,
		"tracked_count": plant_batch.tracked_count,
		"growth_phase": plant_batch.growth_phase,
		"packaged_count": plant_batch.packaged_count,
		"harvested_count": plant_batch.harvested_count,
		"destroyed_count": plant_batch.destroyed_count
	}
	return bloomtrace_plant_batch_dict
