# -*- coding: utf-8 -*-
# Copyright (c) 2018, Bloom Stack and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from bloomstack_core.bloomtrace import make_integration_request

def make_transfer_templates(delivery_trip, method):
	for stop in delivery_trip.delivery_stops:
		if not stop.delivery_note:
			continue

		for item in frappe.get_doc("Delivery Note", stop.delivery_note).items:
			if frappe.db.get_value("Item", item.item_code, "is_compliance_item"):
				make_integration_request("Delivery Note", stop.delivery_note)
				break
