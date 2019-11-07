
from __future__ import unicode_literals
import frappe
import json


def get_notification_config():
	notifications = {"for_doctype": {}}
	if frappe.db.exists("Notification Badges Settings"):
		settings = frappe.get_single("Notification Badges Settings")
        for config in settings.configuration:
            notifications["for_doctype"][config.filter_doctype] = json.loads(config.filter)
	return notifications
