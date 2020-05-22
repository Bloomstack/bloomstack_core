# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import get_url
from urllib.parse import urlparse

class License(Document):
	def before_insert(self):
		client = get_bloomtrace_client()
		if not client:
			return
		site_url = urlparse(get_url()).netloc

		license = client.get_doc("License", self.license_number)
		if not license:
			frappe.throw("Invalid License Number")
		else:
			self.status = license.get("status")
			self.license_issuer = license.get('license_issuer')
			self.license_type = license.get('license_type')
			self.license_category = license.get('license_category')
			self.license_expiry_date = license.get('license_expiry_date')
			self.license_for = license.get('license_for')
			self.legal_name = license.get('legal_name')
			self.county = license.get('county')
			self.city = license.get('city')


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
