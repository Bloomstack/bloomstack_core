# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime, nowdate

class AuthorizationRequest(Document):
	def after_insert(self):
		self.generate_token()
		self.email_link()
		self.status = "Request Sent"

	def generate_token(self):
		self.token = frappe.generate_hash(self.name, 32)
		self.token_generated_on = now_datetime()
		self.request_link = "http://localhost:8000/authorize_document?token={0}&name={1}".format(self.token, self.name)
		self.save()
		
	def email_link(self):
		"""
			Email the document link to user for them to authorize the document
		"""
		message = frappe.render_template("templates/emails/authorization_request.html", {
			"authorization_request": self,
			"link": self.request_link
		})

		frappe.sendmail(recipients=[self.authorizer_email], subject="You have a document to authorize", message=message)
