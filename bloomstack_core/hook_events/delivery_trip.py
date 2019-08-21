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
		if not frappe.db.get_single_value("Google Maps Settings", "enabled"):
			return

		if delivery_trip.delivery_stops:
			route_list = delivery_trip.form_route_list(optimize=False)

			if not route_list:
				return

			route_list = route_list[0]

			context = {
				"key": frappe.db.get_single_value("Google Maps Settings", "client_key"),
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
def make_payment_entry(payment_amount, sales_invoice, delivery_trip):
	payment_entry = get_payment_entry("Sales Invoice", sales_invoice, party_amount=flt(payment_amount))
	payment_entry.paid_amount = payment_amount

	territory = frappe.db.get_value("Sales Invoice", sales_invoice, "territory")
	mode_of_payment = frappe.db.get_value("Territory", territory, "mode_of_payment") or "Cash"

	payment_entry.mode_of_payment = mode_of_payment
	account = get_bank_cash_account(payment_entry.mode_of_payment, payment_entry.company)
	if account:
		payment_entry.paid_to = account.get("account")
	payment_entry.reference_date = today()
	payment_entry.reference_no = delivery_trip
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


def create_timesheet(trip, method):

	def _create_timesheet(trip):
		employee = frappe.get_value("Driver", trip.driver, "employee")
		timesheet = frappe.new_doc("Timesheet")
		timesheet.company = trip.company
		timesheet.employee = employee
		timesheet.append("time_logs", {
			"from_time": trip.odometer_start_time,
			"delivery_trip": trip.name

		})
		timesheet.save()

	def update_timesheet(trip):
		timesheet_list = frappe.get_all("Timesheet Detail", filters={'delivery_trip': trip.name}, fields = ["parent"])
		print("timesheet_detail", timesheet_list)
		if timesheet_list:
			timesheet = timesheet_list[0].get("parent")
			print("timesheet_detail[0].get('parent')", timesheet)
			timesheet = frappe.get_doc("Timesheet", timesheet)
			for time_log in timesheet.time_logs:
				if time_log.from_time and not time_log.to_time:
					time_log.to_time = trip.odometer_end_time
					time_log.activity_type = "Driving"
			timesheet.save()
			if trip.odometer_end_value:
				timesheet.submit()

	if trip.odometer_start_value:
		if trip.odometer_end_value:
			update_timesheet(trip)
		else:
			_create_timesheet(trip)
