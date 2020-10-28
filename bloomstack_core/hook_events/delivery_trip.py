# -*- coding: utf-8 -*-
# Copyright (c) 2018, Bloom Stack and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from requests.utils import quote

import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, nowdate, today
from bloomstack_core.bloomtrace import make_integration_request

def generate_directions_url(delivery_trip, method):
	if method == "validate":
		if not frappe.db.get_single_value("Google Settings", "enable"):
			return

		if not delivery_trip.driver_address:
			return

		if delivery_trip.delivery_stops:
			route_list = delivery_trip.form_route_list(optimize=False)

			if not route_list:
				return

			route_list = route_list[0]

			context = {
				"key": frappe.db.get_single_value("Google Settings", "api_key"),
				"origin": quote(route_list[0], safe=''),
				"destination": quote(route_list[-1], safe=''),
				"waypoints": quote('|'.join(route_list[1:-1]), safe='')
			}

			map_data = frappe.render_template("templates/includes/google_maps_embed.html", context)
			delivery_trip.map_embed = map_data


def link_invoice_against_trip(delivery_trip, method):
	for delivery_stop in delivery_trip.delivery_stops:
		if delivery_stop.delivery_note:
			sales_invoice = frappe.get_all("Delivery Note Item",
				filters={"docstatus": 1, "parent": delivery_stop.delivery_note},
				fields=["against_sales_invoice"],
				distinct=True)
            # set sale invoice for cycle sales order>>sales invoice>>delivery note>>delivery trip
			if sales_invoice and len(sales_invoice) == 1:
				delivery_stop.sales_invoice = sales_invoice[0].against_sales_invoice
			# set sales invoice for cyecle sales order>>Delivery Note >>sales invoice>> then Delivery Trip from Delivery Note
			if sales_invoice[0].against_sales_invoice==None:
				sales_invoice = frappe.get_all("Sales Invoice Item",
				filters={"docstatus": 1, "delivery_note": delivery_stop.delivery_note},
				fields=["distinct(parent)"])
				if len(sales_invoice)==1:
					print("second cycle",sales_invoice)
					delivery_stop.sales_invoice = sales_invoice[0].parent				


def make_transfer_templates(delivery_trip, method):
	for stop in delivery_trip.delivery_stops:
		if not stop.delivery_note:
			continue

		for item in frappe.get_doc("Delivery Note", stop.delivery_note).items:
			if frappe.db.get_value("Item", item.item_code, "is_compliance_item"):
				make_integration_request("Delivery Note", stop.delivery_note)
				break


def set_vehicle_last_odometer_value(trip, method):
	if trip.actual_distance_travelled:
		frappe.db.set_value('Vehicle', trip.vehicle, 'last_odometer', trip.odometer_end_value)


@frappe.whitelist()
def get_address_display(address):
	address_details = frappe.db.get_value("Address", address, "*", as_dict=True)
	return frappe.render_template("erpnext/regional/united_states/address_template.html", address_details)
