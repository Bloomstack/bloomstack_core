# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import get_url
from urllib.parse import urlparse

class ComplianceInfo(Document):
	def before_insert(self):
		client = get_bloomtrace_client()
		if not client:
			return
		site_url = urlparse(get_url()).netloc

		license_info = client.get_doc("License", self.license_number)
		if not license_info:
			frappe.msgprint("License Number not found in our database. Proceed with Caution")
		else:
			self.status = license_info.get("status")
			self.license_issuer = license_info.get('license_issuer')
			self.license_type = license_info.get('license_type')
			self.license_category = license_info.get('license_category')
			self.license_expiry_date = license_info.get('license_expiry_date')
			self.license_for = license_info.get('license_for')
			self.legal_name = license_info.get('legal_name')
			self.county = license_info.get('county')
			self.city = license_info.get('city')


		client_records = client.get_doc("Client", filters={"bloomstack_instance": site_url})
		if client_records:
			client_name = client_records[0].get("name")

			client_customer = {
				"doctype": "Client Customer",
				"client": client_name,
				"license": self.license_number,
				"status": "Active"
			}
			client.insert(client_customer)
