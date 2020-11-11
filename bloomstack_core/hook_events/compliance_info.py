import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import get_host_name


def create_bloomtrace_license(compliance_info, method):
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return
	site_url = get_host_name()

	license_info = frappe_client.get_doc("License Info", compliance_info.license_number)
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
		make_bloomstack_site_license(frappe_client, site_url, compliance_info.license_number, 'Active')


def make_bloomstack_site_license(frappe_client, site_url, license_number, status='Pending Update'):
	if not frappe.get_conf().developer_mode:
		bloomstack_site_license = {
			"doctype": "Bloomstack Site License",
			"bloomstack_site": site_url,
			"license_info": license_number,
			"status": status
		}
		frappe_client.insert(bloomstack_site_license)
