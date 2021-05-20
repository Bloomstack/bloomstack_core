import frappe
from bloomstack_core.bloomtrace import make_integration_request
from frappe import _
from frappe.core.utils import find
from frappe.desk.form.linked_with import get_linked_docs, get_linked_doctypes
from frappe.utils import date_diff, get_time, getdate, nowdate, to_timedelta, today


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


def validate_delivery_window(doc, method):
	from erpnext.stock.doctype.delivery_trip.delivery_trip import get_delivery_window
	if not frappe.db.get_single_value("Delivery Settings", "send_delivery_window_warning"):
		return

	if not (doc.get("delivery_start_time") and doc.get("delivery_end_time")):
		return

	if not doc.get("customer"):
		return

	delivery_window = get_delivery_window(customer=doc.get("customer"))
	delivery_start_time = delivery_window.delivery_start_time
	delivery_end_time = delivery_window.delivery_end_time

	if not (delivery_start_time and delivery_end_time):
		return

	if to_timedelta(doc.delivery_start_time) < to_timedelta(delivery_start_time) \
		or to_timedelta(doc.delivery_end_time) > to_timedelta(delivery_end_time):
		if method == "validate":
			frappe.msgprint(_("The delivery window is set outside the customer's default timings"))
		elif method == "on_submit":
			# send an email notifying users that the document is outside the customer's delivery window
			role_profiles = ["Fulfillment Manager"]
			role_profile_users = frappe.get_all("User", filters={"role_profile_name": ["IN", role_profiles]}, fields=["email"])
			role_profile_users = [user.email for user in role_profile_users]

			accounts_managers = get_users_with_role("Accounts Manager")
			system_managers = get_users_with_role("System Manager")

			recipients = list(set(role_profile_users + accounts_managers) - set(system_managers))

			if not recipients:
				return

			# form the email
			subject = _("[Info] An order may be delivered outside a customer's preferred delivery window")
			message = _("""An order ({name}) has the following delivery window: {doc_start} - {doc_end}<br><br>
				While the default delivery window is {customer_start} - {customer_end}""".format(
					name=frappe.utils.get_link_to_form(doc.doctype, doc.name),
					doc_start=get_time(doc.delivery_start_time).strftime("%I:%M %p"),
					doc_end=get_time(doc.delivery_end_time).strftime("%I:%M %p"),
					customer_start=get_time(delivery_start_time).strftime("%I:%M %p"),
					customer_end=get_time(delivery_end_time).strftime("%I:%M %p"),
				))

			frappe.sendmail(recipients=recipients, subject=subject, message=message)

def get_users_with_role(role):
	# returns users with the specified role
	user_list = frappe.get_all("User", fields=["`tabUser`.name"],
		filters = [
			["Has Role", "role", "=", role],
			["User", "name", "not in", ["Guest", "Administrator"]],
			["User", "enabled", "=", 1]
		],
		as_list=1
	)

	return [user for users in user_list for user in users]