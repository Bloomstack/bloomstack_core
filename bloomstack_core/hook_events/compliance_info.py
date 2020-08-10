from urllib.parse import urlparse

import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import get_url


def create_bloomtrace_license(compliance_info, method):
	client = get_bloomtrace_client()
	if not client:
		return
	site_url = urlparse(get_url()).netloc

	license_info = client.get_doc("License Info", compliance_info.license_number)
	if not license_info:
		frappe.msgprint(
			"License Number not found in our database. Proceed with Caution")
	else:
		compliance_info.status = license_info.get("status")
		compliance_info.license_issuer = license_info.get('issued_by')
		compliance_info.license_type = license_info.get('license_type')
		compliance_info.license_category = license_info.get('license_category')
		compliance_info.license_expiry_date = license_info.get('expiration_date')
		compliance_info.license_for = license_info.get('license_for')
		compliance_info.legal_name = license_info.get('legal_name')
		compliance_info.county = license_info.get('county')
		compliance_info.city = license_info.get('city')

		if not frappe.get_conf().developer_mode:
			bloomstack_site_license = {
				"doctype": "Bloomstack Site License",
				"bloomstack_site": site_url,
				"license_info": compliance_info.license_number,
				"status": "Active"
			}
			client.insert(bloomstack_site_license)
