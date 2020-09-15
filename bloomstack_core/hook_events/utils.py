import frappe
from bloomstack_core.bloomtrace import make_integration_request
from frappe import _
from frappe.core.utils import find
from frappe.desk.form.linked_with import get_linked_docs, get_linked_doctypes
from frappe.utils import date_diff, get_time, getdate, nowdate, to_timedelta, today
from frappe.utils.user import get_users_with_role


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


def validate_expired_licenses(doc, method):
	"""remove expired licenses from company, customer and supplier records"""

	for row in doc.licenses:
		if row.license_expiry_date and row.license_expiry_date < getdate(today()):
			expired_since = date_diff(getdate(today()), getdate(row.license_expiry_date))
			frappe.msgprint(_("Row #{0}: License {1} has expired {2} days ago".format(
				row.idx, frappe.bold(row.license), frappe.bold(expired_since))))


def create_integration_request(doc, method):
	if method == "validate":
		if not doc.is_new():
			make_integration_request(doc.doctype, doc.name)
	elif method == "after_insert":
		make_integration_request(doc.doctype, doc.name)
