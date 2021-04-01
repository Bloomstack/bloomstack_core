import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import get_host_name


def sync_bloomtrace(compliance_settings, method):
	if not compliance_settings.is_compliance_enabled:
		return

	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	site_url = get_host_name()

	try:
		frappe_client.update({
			"doctype": "Bloomstack Site",
			"name": site_url,
			"metrc_user_key": compliance_settings.get_password("metrc_user_key")
		})
	except Exception as e:
		frappe.log_error(e)

	for company in compliance_settings.company:
		try:
			frappe_client.update({
				"doctype": "Bloomstack Company",
				"name": company.company,
				"push_item": company.push_item,
				"pull_item": company.pull_item,
				"push_package_tag": company.push_package_tag,
				"pull_package_tag": company.pull_package_tag,
				"pull_transfer": company.pull_transfer,
				"push_transfer": company.push_transfer,
				"pull_plant": company.pull_plant,
				"push_plant": company.push_plant,
				"pull_plant_batch": company.pull_plant_batch,
				"push_plant_batch": company.push_plant_batch,
				"pull_strain": company.pull_strain,
				"push_strain": company.push_strain,
				"pull_harvest": company.pull_harvest,
				"push_harvest": company.push_harvest,
				"pull_package": company.pull_package,
				"push_package": company.push_package
			})
		except Exception as e:
			frappe.log_error(e)