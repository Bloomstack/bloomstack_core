
from __future__ import unicode_literals
import frappe
import json

def get_notification_config():
    setting = frappe.get_single("Notification Badges Settings")
    notifications = {"for_doctype":{}}
    for config in setting.as_dict().configuration:
        notifications["for_doctype"][config.filter_doctype] = json.loads(config.filter)

    return notifications
