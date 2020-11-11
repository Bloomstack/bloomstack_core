import json

from python_metrc import METRC

import frappe


def get_metrc():
	settings = frappe.get_single("Compliance Settings")

	if not settings.is_compliance_enabled:
		return

	if not all([settings.metrc_url, settings.metrc_vendor_key, settings.metrc_user_key, settings.metrc_vendor_key]):
		frappe.throw("Please configure Compliance Settings")

	return METRC(settings.metrc_url, settings.get_password("metrc_vendor_key"), settings.get_password("metrc_user_key"), settings.metrc_license_no)


def log_request(endpoint, request_data, response, ref_dt=None, ref_dn=None):
	request = frappe.new_doc("API Request Log")
	request.update({
		"endpoint": endpoint,
		"request_body": json.dumps(request_data, indent=4, sort_keys=True),
		"response_code": response.status_code,
		"response_body": json.dumps(response.text, indent=4, sort_keys=True),
		"reference_doctype": ref_dt,
		"reference_document": ref_dn
	})
	request.insert()
	frappe.db.commit()
