from __future__ import unicode_literals
import os

import frappe
from frappe import _


def execute():
	frappe.reload_doc("email", "doctype", "email_template")
	frappe.reload_doc("bloomstack_core", "doctype", "compliance_settings")

	if not frappe.db.exists("Email Template", "License Expiry Alert"):
		base_path = frappe.get_app_path("bloomstack_core", "templates", "emails")
		response = frappe.read_file(os.path.join(base_path, "license_expiry_reminder.html"))

		frappe.get_doc({
			"doctype": "Email Template",
			"name": _("License Expiry Alert"),
			"response": response,
			"subject": _("License Expiry Alert!"),
			"owner": frappe.session.user,
		}).insert(ignore_permissions=True)

	compliance_settings = frappe.get_doc("Compliance Settings")
	compliance_settings.license_expiry_email_template = _("License Expiry Alert")
	compliance_settings.save()
