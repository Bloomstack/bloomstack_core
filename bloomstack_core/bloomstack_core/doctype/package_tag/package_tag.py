# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document
from bloomstack_core.bloomtrace import make_integration_request


class PackageTag(Document):
	def validate(self):
		if self.source_package_tag:
			self.validate_source_package_tag()
			self.update_coa_batch_no()
		if not self.is_new():
			make_integration_request(self.doctype, self.name)

	def after_insert(self):
		make_integration_request(self.doctype, self.name)

	def validate_source_package_tag(self):
		source_package_tag = frappe.db.get_value("Package Tag", self.source_package_tag, "source_package_tag")
		if self.name == source_package_tag:
			frappe.throw(_("Invalid package tag. {0} is already the source package for {1}.".format(self.name, self.source_package_tag)))

	def update_coa_batch_no(self):
		self.coa_batch_no = frappe.db.get_value("Package Tag", self.source_package_tag, "coa_batch_no")
