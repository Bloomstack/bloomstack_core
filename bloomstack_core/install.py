from __future__ import unicode_literals
import os

import frappe
from frappe import _
from frappe.desk.page.setup_wizard.setup_wizard import make_records

def after_install():
	base_path = frappe.get_app_path("bloomstack_core", "templates", "emails")
	response = frappe.read_file(os.path.join(base_path, "license_expiry_reminder.html"))

	records = [{'doctype': 'Email Template', 'name': _("License Expiry Alert"), 'response': response,\
		'subject': _("License Expiry Alert!"), 'owner': frappe.session.user}]

	make_records(records)

	compliance_settings = frappe.get_doc("Compliance Settings")
	compliance_settings.license_expiry_email_template = _("License Expiry Alert")
	compliance_settings.save()