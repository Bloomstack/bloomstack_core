import frappe
from frappe import _
from frappe.core.utils import find
from frappe.utils import getdate, nowdate


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
	
	return license_record


def validate_default_license(doc, method):
	"""allow to set only one default license for supplier or customer"""

	# auto-set default license if only one is found
	if len(doc.licenses) == 1:
		doc.licenses[0].is_default = 1

	# prevent users from setting multiple default licenses
	default_license = [license for license in doc.licenses if license.is_default]
	if len(default_license) != 1:
		frappe.throw(_("There can be only one default license for {0}, found {1}").format(doc.name, len(default_license)))


def get_default_license(party_type, party_name):
	"""get default license from customer or supplier"""

	doc = frappe.get_doc(party_type, party_name)

	licenses = doc.get("licenses")
	if not licenses:
		return

	default_license = find(licenses, lambda license: license.get("is_default")) or ''

	if default_license:
		default_license = default_license.get("license")

	return default_license

@frappe.whitelist()
def filter_license(doctype, txt, searchfield, start, page_len, filters):
	"""filter license"""

	return frappe.get_all('Compliance License Detail',
		filters={
			'parent': filters.get("party_name")
		},
		fields=["name"],
		as_list=1)
