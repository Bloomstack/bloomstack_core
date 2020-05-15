import frappe
from frappe import _

def update_lead_acc_open_date(customer, method):
	"""update lead account opend date"""

	if customer.lead_name and customer.opening_date:
		frappe.db.set_value("Lead", customer.lead_name, "account_opened_date", customer.opening_date)

def validate_default_license(customer, method):
	"""allow to set only one default license"""

	default_license = [license for license in customer.compliance_licenses if license.is_default]
	if len(default_license) != 1:
			frappe.throw(_("There can be only one default license, found {0}").format(len(default_license)))