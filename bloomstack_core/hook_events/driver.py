# -*- coding: utf-8 -*-
# Copyright (c) 2018, Bloom Stack and contributors
# For license information, please see license.txt

import frappe

def get_employee_from_user(driver, method):
	if method == "validate":
		if driver.user_id:
			employee = frappe.db.get_value("Employee", {"user_id": driver.user_id})
			if employee:
				driver.employee = employee
