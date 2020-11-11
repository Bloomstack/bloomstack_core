import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import get_host_name
from bloomstack_core.hook_events.compliance_info import make_bloomstack_site_license


def sync_with_bloomtrace():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return
	site_url = get_host_name()

	clear_bloomstack_site_users(frappe_client, site_url)
	make_bloomstack_site_users()

	clear_bloomstack_site_licenses(frappe_client, site_url)
	make_bloomstack_site_licenses(frappe_client, site_url)


def clear_bloomstack_site_users(frappe_client, site_url):
	bloomstack_site_user = frappe_client.get_doc("Bloomstack Site User", filters={"bloomstack_site": site_url})
	for user in bloomstack_site_user:
		frappe_client.delete("Bloomstack Site User", user.get('name'))


def make_bloomstack_site_users():
	for user in frappe.get_all("User"):
		frappe.get_doc("User", user.name).save()


def clear_bloomstack_site_licenses(frappe_client, site_url):
	bloomstack_site_license = frappe_client.get_doc("Bloomstack Site License", filters={"bloomstack_site": site_url})
	for site_license in bloomstack_site_license:
		frappe_client.delete("Bloomstack Site License", site_license.get('name'))


def make_bloomstack_site_licenses(frappe_client, site_url):
	compliance_info = frappe.get_all("Compliance Info")
	for site_license in compliance_info:
		license_info = frappe_client.get_doc("License Info", site_license.name)
		if license_info:
			make_bloomstack_site_license(frappe_client, site_url, site_license.name)
