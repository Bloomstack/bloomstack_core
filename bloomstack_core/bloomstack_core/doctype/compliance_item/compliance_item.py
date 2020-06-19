# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloomstack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from bloomstack_core.compliance.item import create_item, update_item
from frappe import _
from frappe.model.document import Document


class ComplianceItem(Document):
	def validate(self):
		self.validate_item_category()
		self.validate_existing_metrc_item()
		if not self.is_new() and self.enable_metrc:
			self.sync_metrc_item()
		self.make_bloomtrace_integration_request()

	def after_insert(self):
		self.make_bloomtrace_integration_request()
		if self.enable_metrc:
			self.sync_metrc_item()

	def validate_item_category(self):
		if self.enable_cultivation_tax and not self.item_category:
			frappe.throw(_("Please select an Item Category to enable cultivation tax"))

	def validate_existing_metrc_item(self):
		if self.is_new() and frappe.db.exists("Compliance Item", self.item_code):
			frappe.throw(_("A Compliance Item already exists for {}".format(self.item_code)))

	def sync_metrc_item(self):
		item = frappe.get_doc("Item", self.item_code)

		# Merge Item and Compliance Item data
		item.update(self.as_dict())

		if not self.metrc_id:
			metrc_id = create_item(item)

			if metrc_id:
				frappe.db.set_value("Compliance Item", self.name, "metrc_id", metrc_id)
				frappe.msgprint(_("{} was successfully created in METRC (ID number: {}).".format(item.item_name, metrc_id)))
			else:
				frappe.msgprint(_("{} was successfully created in METRC.".format(item.item_name)))
		else:
			update_item(item)
			frappe.msgprint(_("{} was successfully updated in METRC.".format(item.item_name)))

	def make_bloomtrace_integration_request(self):
		if frappe.get_conf().enable_bloomtrace and not self.is_new():
			integration_request = frappe.new_doc("Integration Request")
			integration_request.update({
				"integration_type": "Remote",
				"integration_request_service": "BloomTrace",
				"status": "Queued",
				"reference_doctype": "Compliance Item",
				"reference_docname": self.name
			})
			integration_request.save(ignore_permissions=True)

def metrc_item_category_query(doctype, txt, searchfield, start, page_len, filters):
	metrc_uom = filters.get("metrc_uom")
	quantity_type = frappe.db.get_value("Compliance UOM", metrc_uom, "quantity_type")

	return frappe.get_all("Compliance Item Category", filters={"quantity_type": quantity_type}, as_list=1)


def metrc_uom_query(doctype, txt, searchfield, start, page_len, filters):
	metrc_item_category = filters.get("metrc_item_category")
	quantity_type = frappe.db.get_value("Compliance Item Category", metrc_item_category, "quantity_type")

	return frappe.get_all("Compliance UOM", filters={"quantity_type": quantity_type}, as_list=1)


def metrc_unit_uom_query(doctype, txt, searchfield, start, page_len, filters):
	metrc_item_category = filters.get("metrc_item_category")
	mandatory_unit = frappe.db.get_value("Compliance Item Category", metrc_item_category, "mandatory_unit")

	quantity_type = None
	if mandatory_unit == "Volume":
		quantity_type = "VolumeBased"
	elif mandatory_unit == "Weight":
		quantity_type = "WeightBased"

	return frappe.get_all("Compliance UOM", filters={"quantity_type": quantity_type}, as_list=1)
