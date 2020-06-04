# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document


class PackageTag(Document):
	def validate(self):
		if self.source_package_tag:
			self.validate_source_package_tag()
		self.make_bloomtrace_integration_request()
	
	def after_insert(self):
		self.make_bloomtrace_integration_request()

	def validate_source_package_tag(self):
		source_package_tag = frappe.db.get_value("Package Tag", self.source_package_tag, "source_package_tag")
		if self.name == source_package_tag:
			frappe.throw(_("Invalid package tag. {0} is already the source package for {1}.".format(self.name, self.source_package_tag)))

	def make_bloomtrace_integration_request(self):
		if frappe.get_conf().enable_bloomtrace and not self.is_new():
			integration_request = frappe.new_doc("Integration Request")
			integration_request.update({
				"integration_type": "Remote",
				"integration_request_service": "BloomTrace",
				"status": "Queued",
				"reference_doctype": "Package Tag",
				"reference_docname": self.name
			})
			integration_request.save(ignore_permissions=True)
