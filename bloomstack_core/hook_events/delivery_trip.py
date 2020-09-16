# -*- coding: utf-8 -*-
# Copyright (c) 2018, Bloom Stack and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from bloomstack_core.bloomtrace import make_integration_request

def make_transfer_templates(delivery_trip, method):
	for stop in delivery_trip.delivery_stops:
		if stop.delivery_note:
			for item in frappe.get_doc("Delivery Note", stop.delivery_note).items:
				if frappe.db.exists("Compliance Item", item.item_code):
					make_integration_request("Delivery Note", stop.delivery_note)
					break

@frappe.whitelist()
def get_address_display(address):
	address_details = frappe.db.get_value("Address", address, "*", as_dict=True)
	return frappe.render_template("erpnext/regional/united_states/address_template.html", address_details)
