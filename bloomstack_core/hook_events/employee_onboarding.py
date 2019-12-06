from __future__ import unicode_literals

import frappe
from frappe import _


def send_emails_to_assigned_users(employee_onboarding, method):

	for activity in employee_onboarding.activities:
		recipients = activity.user
		subject = "An employee onboarding activity has been assigned to you."
		message = "You've been assigned to the activity: {0}".format(str(activity.activity_name))
		frappe.sendmail(recipients=recipients, subject=subject, message=message)
