# Copyright (c) 2013, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe

def execute(filters=None):
	columns= get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	return [
		{
			"fieldname": "customer_name",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 200
		},
		{
			"fieldname": "total_sales",
			"label": _("Total Sales"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 200
		},
		{
			"fieldname": "total_purchase",
			"label": _("Total Purchase"),
			"fieldtype": "Link",
			"options": "Purchase Invoice",
			"width": 200

		},
		{
			"fieldname": "net_gl", #net_gl is Net Gain/Loss
			"label": _("Net Profit/Loss"),
			"width": 200

		}
	]

def get_data(filters=None):
	data= frappe.db.sql("""
	SELECT 
		c.customer_name AS customer_name,
		si.grand_total AS total_sales,
		pi.grand_total AS total_purchase 
	FROM 
		tabCustomer c INNER JOIN 
		tabSupplier s, 
		`tabSales Invoice` si, 
		`tabPurchase Invoice` pi 
	WHERE 
		c.customer_name=s.supplier_name 
	AND 
		si.customer=c.customer_name 
	And 
		pi.supplier=c.customer_name""",as_dict=True)

	for i in data:
		i["net_gl"]= i.total_sales-i.total_purchase 
	return data