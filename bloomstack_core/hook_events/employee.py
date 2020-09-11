# -*- coding: utf-8 -*-
# Copyright (c) 2018, Bloom Stack and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _


def update_driver_employee(employee, method):
	if method == "validate":
		user_id = employee.user_id
		if user_id:
			driver = frappe.db.get_value("Driver", {"user_id": user_id}, "name")
		else:
			driver = frappe.db.get_value("Driver", {"employee": employee.name}, "name")

		if driver:
			frappe.db.set_value("Driver", driver, "employee", employee.name if user_id else None)


def get_data(data):
	for transaction in data.transactions:
		if transaction.get("label") == "Benefit":
			transaction.get("items", []).append("Employee Compensation")

	return data
