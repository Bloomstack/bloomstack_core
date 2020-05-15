import frappe
from frappe import _
from frappe.utils import getdate, nowdate
from frappe.core.utils import find

def validate_license_expiry(doc, method):
	if doc.doctype in ("Quotation", "Sales Order", "Sales Invoice", "Delivery Note"):
		validate_entity_license("Customer", doc.customer)

	elif doc.doctype in ("Purchase Order", "Purchase Invoice", "Purchase Receipt"):
		validate_entity_license("Supplier", doc.supplier)


@frappe.whitelist()
def validate_entity_license(party_type, party_name):
	license_record = get_default_license(party_type, party_name)
	if not license_record:
		return

	license_expiry_date, license_number = frappe.db.get_value(
		"Compliance Info", license_record, ["license_expiry_date", "license_number"])

	if license_expiry_date and license_expiry_date < getdate(nowdate()):
		frappe.throw(_("{0}'s license number {1} has expired on {2}").format(
			frappe.bold(party_name), frappe.bold(license_number), frappe.bold(license_expiry_date)))

def validate_default_license(doc, method):
	"""allow to set only one default license for supplier or customer"""

	default_license = [license for license in doc.compliance_licenses if license.is_default]
	if len(default_license) != 1:
			frappe.throw(_("There can be only one default license, found {0}").format(len(default_license)))

def get_default_license(party_type, party_name):
	"""get default license from customer or supplier"""
	doc = frappe.get_doc(party_type, party_name)
	compliance_licenses = doc.get("compliance_licenses")
	if not compliance_licenses:
		return

	default_license = find(compliance_licenses, lambda gateway: gateway.get("is_default")) or ''

	if default_license:
		default_license = default_license.get("license")

	return default_license