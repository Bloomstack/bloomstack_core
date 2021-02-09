# pylint: disable=W0622

import frappe
from frappe import _
from bloomstack_core.bloomtrace import get_bloomtrace_client
import json

@frappe.whitelist()
def get_all_licenses(filters, limit_start=0, limit_page_length=21):
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		frappe.throw(_("Bloomtrace Integration is disabled."))

	condition_map = {
		"zip_code": {
			"condition": "=",
			"pattern": "{}"
		},
		"license_type": {
			"condition": "=",
			"pattern": "{}"
		},
		"legal_name": {
			"condition": "like",
			"pattern": "%{}%"
		}
	}

	license_filters = {}
	filters = json.loads(filters)
	for key, value in filters.items():
		license_filters.update({
			key: [condition_map.get(key).get("condition"), condition_map.get(key).get("pattern").format(value)]
		})

	params = {
		"cmd": "bloomtrace.bloomtrace.doctype.license_info.license_info.get_licenses",
		"filters": license_filters,
		"fields": ["legal_name", "zip_code", "license_type", "county", "city", "license_number", "email_id", "expiration_date", "status"],
		"limit_start": limit_start,
		"limit_page_length": limit_page_length
	}

	try:
		r = frappe_client.post_request(params)
		return r
	except Exception as e:
		frappe.log_error(e)
		frappe.throw(_("Couldn't connect to BloomTrace."))

@frappe.whitelist()
def get_license_types():
	if not frappe.cache().hget("cannabis", "license_type"):
		fetch_license_types_from_bloomtrace()

	return frappe.cache().hget("cannabis", "license_type")

def fetch_license_types_from_bloomtrace():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		frappe.throw(_("Bloomtrace Integration is disabled."))

	doc = frappe_client.get_doc("DocType", "License Info")

	for field in doc.get("fields", []):
		if field.get("fieldname") == "license_type":
			frappe.cache().hset("cannabis", "license_type", field.get("options"))

	return frappe.cache().hget("cannabis", "license_type")

@frappe.whitelist()
def add_license(license, company):
	license = json.loads(license)

	existing_license = frappe.db.exists("Compliance Info", license.get("license_number"))

	if existing_license:
		return existing_license


	doc = frappe.get_doc({
		"doctype": "Compliance Info",
		"company": company,
		"license_number": license.get("license_number"),
		"license_type": license.get("license_type"),
		"license_category": license.get("license_category"),
		"license_expiry_date": license.get("license_expiry_date"),
		"legal_name": license.get("legal_name"),
		"county": license.get("county"),
		"city": license.get("city"),
		"license_issuer": license.get("license_issuer"),
		"synced_from_bloomtrace": 1
	}).insert(ignore_permissions=True)

	return doc.name

@frappe.whitelist()
def create(source_name, target_doc=None):
	args = frappe.flags.args

	party = frappe.new_doc(args.party)
	party.append("licenses", args.license)

	return party
