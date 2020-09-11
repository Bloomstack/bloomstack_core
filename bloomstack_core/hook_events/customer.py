
# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

import frappe

def update_lead_acc_open_date(customer, method):
	"""update lead account opend date"""

	if customer.lead_name and customer.opening_date:
		frappe.db.set_value("Lead", customer.lead_name, "account_opened_date", customer.opening_date)
