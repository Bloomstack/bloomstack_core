# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import json

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.html_utils import is_json


class NotificationBadgesSettings(Document):
	def validate(self):
		for config in self.configuration:
			self.validate_filter_json(config)
			self.validate_filter_attributes(config)

		frappe.clear_cache()

	def validate_filter_json(self, row):
		if not is_json(row.filter):
			frappe.throw(_("Row {0}: The filter's JSON format is invalid".format(row.idx)))

	def validate_filter_attributes(self, row):
		notification_filter = json.loads(row.filter)
		for attr in notification_filter:
			if not hasattr(frappe.get_meta(row.filter_doctype), attr):
				frappe.throw(_("Row {0}: '{1}' is not a valid attribute in {2}").format(row.idx, attr, row.filter_doctype))
