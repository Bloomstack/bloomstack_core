# -*- coding: utf-8 -*-
# Copyright (c) 2021, Bloomstack Inc. and contributors
# For license information, please see license.txt

import frappe
import json
from bloomstack_core.utils import get_abbr
from erpnext import get_default_company
from erpnext.accounts.utils import get_company_default
from frappe.utils import cstr, get_host_name
from bloomstack_core.bloomtrace import get_bloomtrace_client, make_integration_request
from frappe import _


def create_integration_request(doc, method):
	make_integration_request(doc.doctype, doc.name, "Item")

@frappe.whitelist()
def autoname_item(item):
	config = frappe.get_site_config() or frappe._dict()

	if config.enforce_item_code_naming == True or config.enforce_item_code_naming == None:
		item = frappe._dict(json.loads(item))
		item_code = autoname(item)
		return item_code

	return item.item_code


def autoname(item, method=None):
	"""
		Item Code = a + b + c + d + e, where
			a = abbreviated Company; all caps.
			b = abbreviated Brand; all caps.
			c = abbreviated Item Group; all caps.
			d = abbreviated Item Name; all caps.
			e = variant ID number; has to be incremented.
	"""

	if not frappe.db.get_single_value("Stock Settings", "autoname_item"):
		return

	# Get abbreviations
	item_group_abbr = get_abbr(item.item_group)
	item_name_abbr = get_abbr(item.item_name, 3)
	default_company = get_default_company()

	if default_company:
		company_abbr = get_company_default(default_company, "abbr")
		brand_abbr = get_abbr(item.brand, max_length=len(company_abbr))
		brand_abbr = brand_abbr if company_abbr != brand_abbr else None
		params = list(filter(None, [company_abbr, brand_abbr, item_group_abbr, item_name_abbr]))
		item_code = "-".join(params)
	else:
		brand_abbr = get_abbr(item.brand)
		params = list(filter(None, [brand_abbr, item_group_abbr, item_name_abbr]))
		item_code = "-".join(params)

	# Get count
	count = len(frappe.get_all("Item", filters={"name": ["like", "%{}%".format(item_code)]}))

	if count > 0:
		item_code = "-".join([item_code, cstr(count + 1)])

	# Set item document name
	item.name = item.item_code = item_code

	if not method:
		return item.item_code

def execute_bloomtrace_integration_request():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	pending_requests = frappe.get_all("Integration Request", filters={
		"status": ["IN", ["Queued", "Failed"]],
		"reference_doctype": "Item",
		"integration_request_service": "BloomTrace"
	}, order_by="creation ASC", limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		item = frappe.get_doc("Item", integration_request.reference_docname)

		try:
			if not item.bloomtrace_id:
				insert_compliance_item(item, frappe_client)
			else:
				update_compliance_item(item, frappe_client)

			integration_request.error = ""
			integration_request.status = "Completed"
		except Exception as e:
			integration_request.error = cstr(frappe.get_traceback())
			integration_request.status = "Failed"

		integration_request.save(ignore_permissions=True)


def insert_compliance_item(item, frappe_client):
	bloomtrace_compliance_item_dict = make_compliance_item(item)
	bloomtrace_compliance_item = frappe_client.insert(bloomtrace_compliance_item_dict)
	bloomtrace_id = bloomtrace_compliance_item.get('name')
	frappe.db.set_value("Item", item.name, "bloomtrace_id", bloomtrace_id)


def update_compliance_item(item, frappe_client):
	bloomtrace_compliance_item_dict = make_compliance_item(item)
	bloomtrace_compliance_item_dict.update({
		"name": item.bloomtrace_id
	})
	frappe_client.update(bloomtrace_compliance_item_dict)


def make_compliance_item(item):
	bloomtrace_compliance_item_dict = {
		"doctype": "Compliance Item",
		"bloomstack_site": get_host_name(),
		"item_code": item.item_code,
		"item_name": item.item_name,
		"enable_metrc": item.enable_metrc,
		"metrc_id": item.metrc_id,
		"metrc_item_category": item.metrc_item_category,
		"metrc_unit_value": item.metrc_unit_value,
		"metrc_uom": item.metrc_uom,
		"metrc_unit_uom": item.metrc_unit_uom
	}
	return bloomtrace_compliance_item_dict


# Search querries
def metrc_item_category_query(doctype, txt, searchfield, start, page_len, filters):
	metrc_uom = filters.get("metrc_uom")
	quantity_type = frappe.db.get_value("Compliance UOM", metrc_uom, "quantity_type")

	return frappe.get_all("Compliance Item Category", filters={"quantity_type": quantity_type}, as_list=1)


def metrc_uom_query(doctype, txt, searchfield, start, page_len, filters):
	metrc_item_category = filters.get("metrc_item_category")
	quantity_type = frappe.db.get_value("Compliance Item Category", metrc_item_category, "quantity_type")

	return frappe.get_all("Compliance UOM", filters={"quantity_type": quantity_type}, as_list=1)


def metrc_unit_uom_query(doctype, txt, searchfield, start, page_len, filters):
	metrc_item_category = filters.get("metrc_item_category")
	mandatory_unit = frappe.db.get_value("Compliance Item Category", metrc_item_category, "mandatory_unit")

	quantity_type = "VolumeBased"
	if mandatory_unit == "Weight":
		quantity_type = "WeightBased"

	return frappe.get_all("Compliance UOM", filters={"quantity_type": quantity_type}, as_list=1)
