
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
	frappe_client.update({
		"doctype": "Bloomstack Site",
		"name": site_url,
		"metrc_url": compliance_settings.metrc_url,
		"metrc_user_key": compliance_settings.get_password("metrc_user_key"),
		"metrc_push_data": compliance_settings.metrc_push_data,
		"metrc_pull_data": compliance_settings.metrc_pull_data,
		"pull_incoming_transfer": compliance_settings.pull_incoming_transfer
	})
