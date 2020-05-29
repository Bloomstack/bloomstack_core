import frappe
from frappe import _
from frappe.core.utils import find
from frappe.utils import getdate, nowdate


def validate_license_expiry(doc, method):
	if doc.doctype in ("Sales Order", "Sales Invoice", "Delivery Note"):
		validate_entity_license("Customer", doc.customer)
	elif doc.doctype in ("Supplier Quotation", "Purchase Order", "Purchase Invoice", "Purchase Receipt"):
		validate_entity_license("Supplier", doc.supplier)
	elif doc.doctype == "Quotation" and doc.quotation_to == "Customer":
		validate_entity_license("Customer", doc.party_name)


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

	# remove duplicate licenses
	unique_licenses = list(set([license.license for license in doc.licenses]))
	if len(doc.licenses) != len(unique_licenses):
		frappe.throw(_("Please remove duplicate licenses before proceeding"))

	if len(doc.licenses) == 1:
		# auto-set default license if only one is found
		doc.licenses[0].is_default = 1
	elif len(doc.licenses) > 1:
		default_licenses = [license for license in doc.licenses if license.is_default]
		# prevent users from setting multiple default licenses
		if not default_licenses:
			frappe.throw(_("There must be atleast one default license, found none"))
		elif len(default_licenses) > 1:
			frappe.throw(_("There can be only one default license for {0}, found {1}").format(doc.name, len(default_licenses)))


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
		fields=["license", "is_default", "license_type"],
		as_list=1)

@frappe.whitelist()
def update_timesheets(ref_dt, ref_dn, billable):
	if ref_dt == "Project":
		timesheets = frappe.db.get_all("Timesheet Detail", filters={"project":ref_dn}, fields=["name", "billable"])
	elif ref_dt == "Task":
		timesheets = frappe.db.get_all("Timesheet Detail", filters={"task":ref_dn}, fields=["name", "billable"])

	for time_logs in timesheets:
		frappe.db.set_value("Timesheet Detail", time_logs.name, "billable", billable)