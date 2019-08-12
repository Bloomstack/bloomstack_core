# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document


class ProjectTemplate(Document):
	def validate(self):
		self.validate_task_days()

	def validate_task_days(self):
		for task in self.tasks:
			if task.days_to_task_start and task.days_to_task_start < 0:
				frappe.throw(_("Days to task start must be positive"))

			if task.days_to_task_end and task.days_to_task_end < 0:
				frappe.throw(_("Days to task end must be positive"))

			if task.days_to_task_start and task.days_to_task_end and task.days_to_task_start > task.days_to_task_end:
				frappe.throw(_("Days to task start cannot be after days to task end"))
