from datetime import timedelta

import frappe
from erpnext.accounts.utils import get_balance_on
from frappe.utils import add_days, date_diff, getdate, nowdate


@frappe.whitelist()
def get_insight_engine_dashboards(start_date=None, end_date=None):
	today = nowdate()
	yesterday = add_days(today, -1)
	last_week = add_days(today, -7)
	last_month = add_days(today, -30)

	# Default the dates to a week
	if not end_date:
		end_date = today
	if not start_date:
		start_date = last_week

	date_range = (start_date, end_date)

	yesterdays_revenue = get_revenue_by_date(yesterday)
	weekly_revenue = get_revenue_by_date_range(*date_range)
	monthly_revenue = get_revenue_by_date_range(last_month, end_date)
	top_products = get_top_products(*date_range)
	top_customers = get_top_customers(*date_range)
	top_territories = get_top_territories(*date_range)
	top_sales_partners = get_top_sales_partners(*date_range)
	pending_invoices = get_pending_invoices(*date_range)
	cash_on_hand = get_cash_on_hand()

	return {
		"yesterday_revenue": yesterdays_revenue,
		"total_weekly_revenue": weekly_revenue.get("total", 0),
		"average_weekly_revenue": weekly_revenue.get("average", 0),
		"total_monthly_revenue": monthly_revenue.get("total", 0),
		"average_monthly_revenue": monthly_revenue.get("average", 0),
		"top_customers_by_revenue": top_customers.get("by_revenue"),
		"top_territories_by_revenue": top_territories.get("by_revenue"),
		"top_sales_partners_by_revenue": top_sales_partners.get("by_revenue"),
		"top_products_by_revenue": top_products.get("by_revenue"),
		"top_products_by_volume": top_products.get("by_volume"),
		"top_products_by_time": top_products.get("by_time"),
		"paid_invoices": pending_invoices.get("paid_invoices"),
		"unpaid_invoices": pending_invoices.get("unpaid_invoices"),
		"overdue_invoices": pending_invoices.get("overdue_invoices"),
		"returned_invoices": pending_invoices.get("returned_invoices"),
		"credit_invoices": pending_invoices.get("credit_invoices"),
		"cash_on_hand": cash_on_hand
	}


def get_revenue_by_date(date):
	return frappe.db.get_value("Payment Entry",
		{"posting_date": date, "docstatus": 1, "payment_type": "Receive"},
		"sum(paid_amount)")


def get_revenue_by_date_range(start_date, end_date):
	payments = frappe.get_all("Payment Entry",
		{"posting_date": ["BETWEEN", [start_date, end_date]], "docstatus": 1, "payment_type": "Receive"},
		["sum(paid_amount) AS paid_amount"])

	paid_amount = 0
	if payments:
		paid_amount = payments[0].paid_amount or 0

	average = paid_amount / date_diff(end_date, start_date)

	return {
		"total": paid_amount,
		"average": average
	}


def get_cash_on_hand():
	cash_accounts = frappe.get_all("Account", filters={"account_type": "Cash", "root_type": "Asset", "is_group": 0})
	cash_on_hand = sum([get_balance_on(account.name) for account in cash_accounts])
	return cash_on_hand


def get_top_products(start_date, end_date, limit=10):
	invoice_items_by_name = frappe.db.sql("""
		SELECT
			si_item.item_name AS item,
			SUM(si_item.net_amount) AS revenue,
			SUM(si_item.qty) AS volume
		FROM
			`tabSales Invoice` si
				LEFT JOIN `tabSales Invoice Item` si_item
					ON si.name = si_item.parent
		WHERE
			si.docstatus = 1
				AND si.posting_date BETWEEN %(start_date)s AND %(end_date)s
		GROUP BY
			si_item.item_name
	""", {
		"start_date": start_date,
		"end_date": end_date
	}, as_dict=True)

	top_products_by_revenue = sorted(invoice_items_by_name, key=lambda item: item.revenue, reverse=True)[:limit]
	top_products_by_volume = sorted(invoice_items_by_name, key=lambda item: item.volume, reverse=True)[:limit]
	top_products = list(map(lambda d: d.get("item"), top_products_by_revenue))[:5]

	invoice_items_by_date = frappe.db.sql("""
		SELECT
			si.posting_date AS date,
			si_item.item_name AS item,
			si_item.net_amount AS revenue,
			si_item.qty AS volume
		FROM
			`tabSales Invoice` si
				LEFT JOIN `tabSales Invoice Item` si_item
					ON si.name = si_item.parent
		WHERE
			si.docstatus = 1
				AND si.posting_date BETWEEN %(start_date)s AND %(end_date)s
				AND si_item.item_name IN %(top_products)s
		ORDER BY
			si.posting_date ASC
	""", {
		"start_date": start_date,
		"end_date": end_date,
		"top_products": top_products
	}, as_dict=True)

	# Form a list of dates between the start and end dates
	total_days = date_diff(end_date, start_date)
	date_list = [getdate(start_date) + timedelta(days=x) for x in range(total_days)]

	# Form a dictionary of items and list of sales per day
	top_products_by_time_and_revenue = {}
	for product in top_products:
		top_products_by_time_and_revenue[product] = {date: 0 for date in date_list}

	for invoice in invoice_items_by_date:
		# Ensure only invoices with the requested dates get calculated
		if top_products_by_time_and_revenue.get(invoice.item, {}).has_key(invoice.date):
			top_products_by_time_and_revenue[invoice.item][invoice.date] += invoice.revenue

	# NOTE: Doing dates.values() returns a list of values in an arbitrary order
	# ref: https://docs.python.org/2/library/stdtypes.html#dict.items
	# Using list-comp with a sorted dict to get the values in right order
	top_products_by_time_and_revenue = {
		item: [dates.get(date) for date in sorted(dates)]
			for item, dates in top_products_by_time_and_revenue.items()
	}

	return {
		"by_revenue": top_products_by_revenue,
		"by_volume": top_products_by_volume,
		"by_time": top_products_by_time_and_revenue
	}


def get_top_customers(start_date, end_date, limit=10):
	customers = get_invoices_by_field("customer", start_date, end_date)

	return {
		"by_revenue": sorted(customers, key=lambda customer: customer.grand_total, reverse=True)[:limit]
	}


def get_top_territories(start_date, end_date, limit=5):
	territories = get_invoices_by_field("territory", start_date, end_date)

	return {
		"by_revenue": sorted(territories, key=lambda customer: customer.grand_total, reverse=True)[:limit]
	}


def get_top_sales_partners(start_date, end_date, limit=5):
	sales_partners = get_invoices_by_field("sales_partner", start_date, end_date)

	return {
		"by_revenue": sorted(sales_partners, key=lambda partner: partner.grand_total, reverse=True)[:limit]
	}


def get_pending_invoices(start_date, end_date):
	invoices = get_invoices_by_field("status", start_date, end_date)

	def get_invoice_totals_by_status(status):
		return next((invoice.grand_total for invoice in invoices if invoice.status == status), 0)

	paid_invoices = get_invoice_totals_by_status("Paid")
	unpaid_invoices = get_invoice_totals_by_status("Unpaid")
	overdue_invoices = get_invoice_totals_by_status("Overdue")
	returned_invoices = get_invoice_totals_by_status("Return")
	credit_invoices = get_invoice_totals_by_status("Credit Note Issued")

	return {
		"paid_invoices": paid_invoices,
		"unpaid_invoices": unpaid_invoices,
		"overdue_invoices": overdue_invoices,
		"returned_invoices": returned_invoices,
		"credit_invoices": credit_invoices
	}


def get_invoices_by_field(field, start_date, end_date):
	invoices = frappe.get_all("Sales Invoice",
		filters={"posting_date": ["BETWEEN", [start_date, end_date]], "docstatus": 1},
		fields=[field, "SUM(grand_total) AS grand_total"],
		group_by=field)

	return invoices
