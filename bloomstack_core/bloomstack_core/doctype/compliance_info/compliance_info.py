# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import getdate
from frappe.model.document import Document

class ComplianceInfo(Document):
	pass

def send_alert_for_license_expiry():
	"""
		send alert to companies whoes license expiry date is within next 15 days
	"""
	for company in frappe.get_all("Compliance Info", fields=['license_number', 'license_expiry_date', 'entity', 'entity_type']):
		if get_advance_expiry_date(company.license_expiry_date) == 15:
			email_id = frappe.db.get_value(company.entity_type, company.entity, ['email_id'])
			send_reminder(company.entity, email_id)

def send_reminder(company, email_id):
	"""
		send email to the compnaies for license expiry
	"""
	message = frappe.render_template("foundation/templates/emails/license_expiry_reminder.md", {'title': company})
	frappe.sendmail(recipients=email_id, subject="About liecnse Expiry", message=message)

def  get_advance_expiry_date(expiry_date):
	"""
		return diffenernce between current date and expiry date
	"""
	return (getdate(expiry_date) - getdate()).days