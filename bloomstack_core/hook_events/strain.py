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
		filters={"status": ["IN", ["Queued", "Failed"]], "reference_doctype": "Strain", "integration_request_service": "BloomTrace"},
		order_by="creation ASC",
		limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		strain = frappe.get_doc("Strain", integration_request.reference_docname)
		bloomtrace_strain = frappe_client.get_doc("Strain", integration_request.reference_docname)
		try:
			if not bloomtrace_strain:
				insert_strain(strain, frappe_client)
			else:
				update_strain(strain, frappe_client)
			integration_request.error = ""
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)
		except Exception as e:
			integration_request.error = cstr(e)
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)

def insert_strain(strain, frappe_client):
	bloomtrace_strain = make_strain(strain)
	frappe_client.insert(bloomtrace_strain)

def update_strain(strain, frappe_client):
	bloomtrace_strain = make_strain(strain)
	bloomtrace_strain.update({
		"name": strain.name
	})
	frappe_client.update(bloomtrace_strain)

def make_strain(strain):
	site_url = frappe.utils.get_host_name()
	bloomtrace_strain_dict = {
		"doctype": "Strain",
		"bloomstack_site": site_url,
		"strain": strain.strain_name,
		"indica_percentage": strain.indica_percentage,
		"sativa_percentage": strain.sativa_percentage
	}
	return bloomtrace_strain_dict
