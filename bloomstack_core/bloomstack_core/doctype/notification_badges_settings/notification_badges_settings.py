# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class NotificationBadgesSettings(Document):
	def validate(self):
		invalid_filter_rows = []
		for i in self.as_dict().configuration:
			if not frappe.utils.html_utils.is_json(i.filter):
				invalid_filter_rows.append(self.as_dict().configuration.index(i)+1)
		if invalid_filter_rows:
			invalid_rows = ",".join(str(e) for e in invalid_filter_rows)
			frappe.throw(_("The json format for filter is invalid in row(s) " + invalid_rows))
