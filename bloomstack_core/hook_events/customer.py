import frappe
from erpnext.accounts.utils import get_fiscal_year
from frappe.utils import nowdate
from frappe.utils import (add_days, getdate, formatdate, date_diff,
	add_years, get_timestamp, nowdate, flt)	

def update_lead_acc_open_date(customer, method):
	"""update lead account opend date"""

	if customer.lead_name and customer.opening_date:
		frappe.db.set_value("Lead", customer.lead_name, "account_opened_date", customer.opening_date)

def update_customer_dashboard(customer, method):
	info = get_dashboard_info(customer.doctype, customer.name)
	customer.set_onload('dashboard_info', info)

def get_dashboard_info(party_type, party):
	current_fiscal_year = get_fiscal_year(nowdate(), as_dict=True)

	doctype = "Sales Order"
	companies = frappe.get_all(doctype, filters={
		'docstatus': 1,
		party_type.lower(): party
	}, distinct=1, fields=['company'])

	company_wise_info = []

	company_wise_grand_total = frappe.get_all(doctype,
		filters={
			'docstatus': 1,
			party_type.lower(): party,
			'order_type': 'Marketing',
			'transaction_date': ('between', [current_fiscal_year.year_start_date, current_fiscal_year.year_end_date])
			},
			group_by="company",
			fields=["company", "sum(grand_total) as grand_total", "sum(base_grand_total) as base_grand_total"],
		debug=True)

	company_wise_billing_this_year = frappe._dict()

	for d in company_wise_grand_total:
		company_wise_billing_this_year.setdefault(
			d.company,{
				"grand_total": d.grand_total,
				"base_grand_total": d.base_grand_total
			})

	for d in companies:
		company_default_currency = frappe.db.get_value("Company", d.company, 'default_currency')
		party_account_currency = get_party_account_currency(party_type, party, d.company)

		if party_account_currency==company_default_currency:
			billing_this_year = flt(company_wise_billing_this_year.get(d.company,{}).get("base_grand_total"))
		else:
			billing_this_year = flt(company_wise_billing_this_year.get(d.company,{}).get("grand_total"))

		info = {}
		info["marketing_expense"] = flt(billing_this_year) if billing_this_year else 0
		info["currency"] = party_account_currency
		info["company"] = d.company

		company_wise_info.append(info)

	return company_wise_info

def get_party_account_currency(party_type, party, company):
	def generator():
		party_account = get_party_account(party_type, party, company)
		return frappe.db.get_value("Account", party_account, "account_currency", cache=True)

	return frappe.local_cache("party_account_currency", (party_type, party, company), generator)
