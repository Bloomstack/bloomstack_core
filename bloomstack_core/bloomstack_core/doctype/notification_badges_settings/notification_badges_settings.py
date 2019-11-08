# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import json
from frappe.model.document import Document


class NotificationBadgesSettings(Document):
	def validate(self):
		if self.configuration:
			for i in self.as_dict().configuration:
				invalid_filter_rows = self.validate_filter_json(i)

			if invalid_filter_rows:
				invalid_rows = ",".join(str(e) for e in invalid_filter_rows)
				frappe.throw(_("The json format for filter is invalid in row(s) " + invalid_rows))

	def validate_filter_json(self, row):
		invalid_filter_rows = []
		if frappe.utils.html_utils.is_json(row.filter):
			self.validate_filter_attributes(row)
		else:
			invalid_filter_rows.append(self.as_dict().configuration.index(row)+1)
		return invalid_filter_rows

	def validate_filter_attributes(self, row):
		filter = json.loads(row.filter)
		for key in filter.keys():
			if not hasattr(frappe.get_meta(row.filter_doctype), key):
				frappe.throw(_("The Filter in row '{0}' is invalid").format(
					self.as_dict().configuration.index(row)+1))
