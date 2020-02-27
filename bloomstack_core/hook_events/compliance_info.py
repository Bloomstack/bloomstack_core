import frappe
from erpnext import get_default_company
from frappe import _
from frappe.utils import date_diff, getdate


def send_license_expiry_reminder():
	"""
		Sends alerts about companies whose licenses are about to expire
	"""

	company_email = frappe.db.get_value("Company", get_default_company(), "email")
	expiry_reminder_days = frappe.db.get_single_value("Compliance Settings", "license_expiry_reminder_before_days")
	interval_days = frappe.db.get_single_value("Compliance Settings", "send_email_interval_of_days")

	if not all([company_email, expiry_reminder_days, interval_days]):
		return

	for entity in frappe.get_all("Compliance Info", fields=['license_number', 'license_expiry_date', 'entity', 'entity_type']):
		# Check if expiry date is in the set range
		if date_diff(entity.license_expiry_date, getdate()) in range(expiry_reminder_days, 1, -interval_days):
			entity_email, is_send_enabled = frappe.db.get_value(entity.entity_type, entity.entity, ['email_id', 'send_license_expiry_reminder'])

			# Send out the license expiry reminder to the license holder
			if is_send_enabled:
				_send_reminder(entity_email, entity)

			# Send out the license expiry reminder to the company
			if entity.entity_type != "Company":
				_send_reminder(company_email, entity)


def _send_reminder(email_id, entity):
	license_expiry_email_template = frappe.db.get_single_value("Compliance Settings", "license_expiry_email_template")

	if license_expiry_email_template:
		email_template = frappe.get_doc("Email Template", license_expiry_email_template)
		subject = frappe.render_template(email_template.subject, entity)
		message = frappe.render_template(email_template.response, entity)
	else:
		subject = _("License Expiry Alert")
		message = "License number {0} will expire on {1}".format(entity.license_number, entity.license_expiry_date)

	frappe.sendmail(recipients=email_id, subject=subject, message=message)
