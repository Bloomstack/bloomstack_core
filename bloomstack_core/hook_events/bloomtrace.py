# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import get_host_name
from bloomstack_core.hook_events.compliance_info import make_bloomstack_site_license

def sync_with_bloomtrace():
	frappe_client = get_bloomtrace_client()

	if not frappe_client:
		return

	clear_bloomstack_site_users(frappe_client, get_host_name())
	make_bloomstack_site_users()

	clear_bloomstack_site_licenses(frappe_client, get_host_name())
	make_bloomstack_site_licenses(frappe_client, get_host_name())


def clear_bloomstack_site_users(frappe_client, site_url):

	for user in frappe_client.get_doc("Bloomstack Site User", filters={"bloomstack_site": site_url}):
		frappe_client.delete("Bloomstack Site User", user.get('name'))

def make_bloomstack_site_users():

	for user in frappe.get_all("User"):
		frappe.get_doc("User", user.name).save()

def clear_bloomstack_site_licenses(frappe_client, site_url):

	for site_license in frappe_client.get_doc("Bloomstack Site License", filters={"bloomstack_site": site_url}):
		frappe_client.delete("Bloomstack Site License", site_license.get('name'))

def make_bloomstack_site_licenses(frappe_client, site_url):

	for site_license in frappe.get_all("Compliance Info"):
		if frappe_client.get_doc("License Info", site_license.name):
			make_bloomstack_site_license(frappe_client, site_url, site_license.name)
