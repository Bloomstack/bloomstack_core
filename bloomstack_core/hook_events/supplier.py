import frappe
from frappe import _

def validate_default_license(supplier, method):
	"""allow to set only one default license"""

	default_license = [license for license in supplier.compliance_licenses if license.is_default]
	if len(default_license) != 1:
			frappe.throw(_("There can be only one default license, found {0}").format(len(default_license)))