# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

from urllib.parse import urlparse
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
		filters={"status": ["IN", ["Queued", "Failed"]], "reference_doctype": "Plant", "integration_request_service": "BloomTrace"},
		order_by="creation ASC",
		limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		plant = frappe.get_doc("Plant", integration_request.reference_docname)
		bloomtrace_plant = frappe_client.get_doc("Plant", integration_request.reference_docname)
		try:
			if not bloomtrace_plant:
				insert_plant(plant, frappe_client)
			else:
				update_plant(plant, frappe_client)
			integration_request.error = ""
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)
		except Exception as e:
			integration_request.error = cstr(e)
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)

def insert_plant(plant, frappe_client):
	bloomtrace_plant = make_plant(plant)
	frappe_client.insert(bloomtrace_plant)

def update_plant(plant, frappe_client):
	bloomtrace_plant = make_plant(plant)
	bloomtrace_plant.update({
		"name": plant.name
	})
	frappe_client.update(bloomtrace_plant)

def make_plant(plant):
	site_url = frappe.utils.get_host_name()
	bloomtrace_plant_dict = {
		"doctype": "Plant",
		"bloomstack_site": site_url,
		"label":plant.title,
		"plant_batch_name": plant.plant_batch,
		"strain_name": plant.strain,
		"location_name": plant.location,
		"growth_phase": plant.growth_phase,
		"harvest_count": plant.harvested_count
	}
	return bloomtrace_plant_dict
