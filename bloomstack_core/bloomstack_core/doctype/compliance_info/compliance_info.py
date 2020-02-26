# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import getdate, date_diff
from frappe.model.document import Document

class ComplianceInfo(Document):
	pass

def send_alert_for_license_expiry():
	"""
		send alert to companies whoes license expiry date is within next 15 days
	"""
	for company in frappe.get_all("Compliance Info", fields=['license_number', 'license_expiry_date', 'entity', 'entity_type']):
		before_days = frappe.db.get_single_value("Compliance Settings", "license_expiry_reminder_before_days")
		interval_of = frappe.db.get_single_value("Compliance Settings", "send_email_interval_of_days")
		if company.entity_type == "Company":
			email_id = frappe.db.get_value(company.entity_type, company.entity, ['email'])
		for alternative_days in range(before_days, 1, interval_of):
			if get_advance_expiry_date(company.license_expiry_date) == alternative_days:
				entity_email_id = frappe.db.get_value(company.entity_type, company.entity, ['email_id', 'send_license_expiry_alert'], as_dict=True)
				if entity_email_id.send_license_expiry_alert:
					send_reminder(entity_email_id.email_id, company)
				send_reminder(email_id, company)

def send_reminder(email_id, company):
	"""
		send email to the compnaies for license expiry
	"""
	message = frappe.render_template("foundation/templates/emails/license_expiry_reminder.md", {'title': company.entity })
	frappe.sendmail(recipients=email_id, subject="About liecnse Expiry", message=message)

def  get_advance_expiry_date(expiry_date):
	"""
		return difference between current date and expiry date
	"""
	return date_diff(expiry_date, getdate())