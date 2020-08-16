import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
import json

@frappe.whitelist()
def get_all_licenses(page_number, per_page, filters):
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
			return

	key_map = {
		"zip": {"key": "zip_code", "operator": "=", "pattern": "{}"},
		"licenseType": {"key": "license_type", "operator": "=", "pattern": "{}"},
		"search": {"key": "legal_name", "operator": "like", "pattern": "%{}%"}
	}

	and_filters = {}
	filters = json.loads(filters)
	for f in filters:
		if filters[f] == "":
			continue

		and_filters[key_map[f]["key"]] = [
			key_map[f]["operator"],
			key_map[f]["pattern"].format(filters[f])
		]

	fields = [
		"legal_name",
		"zip_code",
		"license_type",
		"status",
		"county",
		"city",
		"license_number",
		"email_id",
		"expiration_date",
		"business_structure",
		"business_owner",
		"license_for"
	]

	limit_start = (int(page_number)-1) * int(per_page)
	license_info = frappe_client.get_list("License Info", fields=fields,filters=and_filters, limit_start=limit_start, limit_page_length=per_page)

	total_licenses = frappe_client.post_api("frappe.client.get_count", {
		"doctype": "License Info",
		"filters": and_filters
	})

	license_doc = frappe_client.get_doc("DocType", "License Info")
	for field in license_doc["fields"]:
		if field["fieldname"] == 'license_type':
			license_types = field["options"].splitlines()

	return {
		"license_info": license_info,
		"total_count": total_licenses,
		"license_types": license_types
	}
