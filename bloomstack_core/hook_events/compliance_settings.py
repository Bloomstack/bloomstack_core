# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import json

from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import get_host_name
from frappe.installer import get_site_config_path

def sync_bloomtrace(compliance_settings, method):
	if not compliance_settings.is_compliance_enabled:
		return

	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	if frappe_client.get_list("Bloomstack Site", filters={"name": get_host_name()}):
		update_site_details_in_bloomtrace("update", compliance_settings.metrc_url, compliance_settings.get_password("metrc_user_key"),
			compliance_settings.metrc_push_data, compliance_settings.metrc_pull_data)
	else:
		update_site_details_in_bloomtrace("insert", compliance_settings.metrc_url, compliance_settings.get_password("metrc_user_key"),
			compliance_settings.metrc_push_data, compliance_settings.metrc_pull_data)

	pwd = create_user_for_bloomtrace()


def create_user_for_bloomtrace():
	pwd = frappe.generate_hash()

	with open(get_site_config_path(), 'w+') as f:
		update_site_details_in_bloomtrace()

	user = frappe.get_doc({
		"doctype": "User",
		"email": "api@bloomtrace.com",
		"first_name": "Bloomtrace",
		"last_name": "API",
		"send_welcome_email": False,
		"username": "Bloomtrace API",
		"__new_password": pwd,
	}).insert()

	return pwd

def update_password_for_frappe_client(frappe_client, pwd):
	frappe_client

def update_site_details_in_bloomtrace(method, frappe_client, metrc_url, metrc_user_key, metrc_pull_data, metrc_push_data, client_pwd):

	frappe_client[method]({
		"doctype": "Bloomstack Site",
		"name": get_host_name(),
		"site_url": get_host_name(),
		"metrc_url": metrc_url,
		"metrc_user_key": metrc_user_key,
		"metrc_push_data": metrc_push_data,
		"metrc_pull_data": metrc_pull_data
	})