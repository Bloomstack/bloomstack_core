# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from frappe.utils.data import get_url
from erpnext import get_default_company

class AuthorizationRequest(Document):
	def after_insert(self):
		self.generate_token()
		self.send_authorization_request()
		self.status = "Request Sent"

	def generate_token(self):
		self.token = frappe.generate_hash(self.name, 32)
		self.token_generated_on = now_datetime()
		self.request_link = "{0}/authorize_document?token={1}&name={2}".format(get_url(), self.token, self.name)
		self.save()

	def send_authorization_request(self):
		"""
			Email the link to user for them to authorize the document
		"""

		doc = frappe.get_doc(self.linked_doctype, self.linked_docname)
		company = doc.company_name 

		subject = "{0} requests your authorization on {1}".format(company, self.linked_doctype)
		message = frappe.render_template("templates/emails/authorization_request.html", {
			"authorization_request": self,
			"linked_doc": doc,
			"company": company
		})

		frappe.sendmail(recipients=[self.authorizer_email], subject=subject, message=message)