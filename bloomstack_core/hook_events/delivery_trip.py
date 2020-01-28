# -*- coding: utf-8 -*-
# Copyright (c) 2018, Bloom Stack and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from requests.utils import quote

import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
from erpnext.accounts.party import get_due_date
from frappe.utils import flt, nowdate, today
from frappe.model.mapper import get_mapped_doc


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
			sales_invoice = frappe.get_all("Delivery Note Item", filters={"docstatus":1, "parent": delivery_stop.delivery_note},fields=["distinct(against_sales_invoice)"])
			if sales_invoice and len(sales_invoice)==1:
				delivery_stop.sales_invoice = sales_invoice[0].against_sales_invoice


@frappe.whitelist()
def make_payment_entry(payment_amount, sales_invoice):
	payment_entry = get_payment_entry("Sales Invoice", sales_invoice, party_amount=flt(payment_amount))
	payment_entry.paid_amount = payment_amount
	payment_entry.reference_date = today()
	payment_entry.reference_no = sales_invoice
	payment_entry.flags.ignore_permissions = True
	payment_entry.save()

	return payment_entry.name


@frappe.whitelist()
def update_payment_due_date(sales_invoice):
	invoice = frappe.get_doc("Sales Invoice", sales_invoice)

	if not invoice.payment_terms_template:
		return

	due_date = get_due_date(invoice.posting_date, "Customer", invoice.customer, bill_date=frappe.utils.add_days(nowdate(), 7))

	# Update due date in both parent and child documents
	invoice.due_date = due_date
	for term in invoice.payment_schedule:
		term.due_date = due_date

	invoice.save()


def set_vehicle_last_odometer_value(trip, method):
	if trip.actual_distance_travelled:
		frappe.db.set_value('Vehicle', trip.vehicle, 'last_odometer', trip.odometer_end_value)


@frappe.whitelist()
def create_or_update_timesheet(trip, action, odometer_value=None):
	delivery_trip = frappe.get_doc("Delivery Trip", trip)
	time = frappe.utils.now()

	def get_timesheet():
		timesheet_list = frappe.get_all("Timesheet", filters={'docstatus': 0, 'delivery_trip': delivery_trip.name})
		if timesheet_list:
			return frappe.get_doc("Timesheet", timesheet_list[0].name)

	if action == "start":
		employee = frappe.get_value("Driver", delivery_trip.driver, "employee")
		timesheet = frappe.new_doc("Timesheet")
		timesheet.company = delivery_trip.company
		timesheet.employee = employee
		timesheet.delivery_trip = delivery_trip.name
		timesheet.append("time_logs", {
			"from_time": time,
			"activity_type": frappe.db.get_single_value("Delivery Settings", "default_activity_type")
		})
		timesheet.save()

		frappe.db.set_value("Delivery Trip", trip, "status", "In Transit", update_modified=False) # Because we can't status as allow on submit
		frappe.db.set_value("Delivery Trip", trip, "odometer_start_value", odometer_value, update_modified=False)
		frappe.db.set_value("Delivery Trip", trip, "odometer_start_time", time, update_modified=False)
	elif action == "pause":
		timesheet = get_timesheet()

		if timesheet and len(timesheet.time_logs) > 0:
			last_timelog = timesheet.time_logs[-1]

			if last_timelog.activity_type == frappe.db.get_single_value("Delivery Settings", "default_activity_type"):
				if last_timelog.from_time and not last_timelog.to_time:
					last_timelog.to_time = time
					timesheet.save()

		frappe.db.set_value("Delivery Trip", trip, "status", "Paused", update_modified=False)
	elif action == "continue":
		timesheet = get_timesheet()

		if timesheet and len(timesheet.time_logs) > 0:
			last_timelog = timesheet.time_logs[-1]

			if last_timelog.activity_type == frappe.db.get_single_value("Delivery Settings", "default_activity_type"):
				if last_timelog.from_time and last_timelog.to_time:
					timesheet.append("time_logs", {
						"from_time": time,
						"activity_type": frappe.db.get_single_value("Delivery Settings", "default_activity_type")
					})
					timesheet.save()

		frappe.db.set_value("Delivery Trip", trip, "status", "In Transit", update_modified=False)
	elif action == "end":
		timesheet = get_timesheet()

		if timesheet and len(timesheet.time_logs) > 0:
			last_timelog = timesheet.time_logs[-1]

			if last_timelog.activity_type == frappe.db.get_single_value("Delivery Settings", "default_activity_type"):
				last_timelog.to_time = time
				timesheet.save()
				timesheet.submit()

		frappe.db.set_value("Delivery Trip", trip, "status", "Completed", update_modified=False)
		frappe.db.set_value("Delivery Trip", trip, "odometer_end_value", odometer_value, update_modified=False)
		frappe.db.set_value("Delivery Trip", trip, "odometer_end_time", time, update_modified=False)

		start_value = frappe.db.get_value("Delivery Trip", trip, "odometer_start_value")
		frappe.db.set_value("Delivery Trip", trip, "actual_distance_travelled", flt(odometer_value) - start_value, update_modified=False)
