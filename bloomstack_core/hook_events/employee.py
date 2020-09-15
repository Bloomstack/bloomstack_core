from __future__ import unicode_literals

import frappe
from frappe import _


def get_data(data):
	for transaction in data.transactions:
		if transaction.get("label") == "Benefit":
			transaction.get("items", []).append("Employee Compensation")

	return data
