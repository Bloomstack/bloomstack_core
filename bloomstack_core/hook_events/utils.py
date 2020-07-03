import frappe
from frappe import _
from frappe.core.utils import find
from frappe.desk.form.linked_with import get_linked_docs, get_linked_doctypes
from frappe.utils import date_diff, get_time, getdate, nowdate, to_timedelta, today, unique
from frappe.utils.user import get_users_with_role


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

	if not license_expiry_date:
		frappe.msgprint(_("We could not verify the status of license number {0}, Proceed with Caution.").format(frappe.bold(license_number)))
	elif license_expiry_date < getdate(nowdate()):
		frappe.msgprint(_("Our records indicate {0}'s license number {1} has expired on {2}, Proceed with Caution.").format(
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


def validate_expired_licenses(doc, method):
	"""remove expired licenses from company, customer and supplier records"""

	for row in doc.licenses:
		if row.license_expiry_date and row.license_expiry_date < getdate(today()):
			expired_since = date_diff(getdate(today()), getdate(row.license_expiry_date))
			frappe.msgprint(_("Row #{0}: License {1} has expired {2} days ago".format(
				row.idx, frappe.bold(row.license), frappe.bold(expired_since))))


def validate_delivery_window(doc, method):
	if not (doc.get("delivery_start_time") and doc.get("delivery_end_time")):
		return

	if doc.get("customer"):
		delivery_start_time = frappe.db.get_value("Customer", doc.get("customer"), "delivery_start_time")
		delivery_end_time = frappe.db.get_value("Customer", doc.get("customer"), "delivery_end_time")

		if not (delivery_start_time and delivery_end_time):
			return

		if method == "validate":
			if to_timedelta(doc.delivery_start_time) < delivery_start_time \
				or to_timedelta(doc.delivery_end_time) > delivery_end_time:
				frappe.msgprint(_("The delivery window is set outside the customer's default timings"), indicator="orange", alert=True)
		elif method == "on_submit":
			# send an email notifying users that the document is outside the customer's delivery window
			role_profiles = ["Fulfillment Manager"]
			role_profile_users = frappe.get_all("User", filters={"role_profile_name": ["IN", role_profiles]}, fields=["email"])
			role_profile_users = [user.email for user in role_profile_users]

			accounts_managers = get_users_with_role("Accounts Manager")
			recipients = unique(role_profile_users + accounts_managers)

			if not recipients:
				return

			# form the email
			subject = _("[Info] An order may be delivered outside a customer's preferred delivery window")
			message = _("""An order ({name}) has the following delivery window: {doc_start} - {doc_end}<br><br>
				While the customer's preferred delivery window is {customer_start} - {customer_end}""".format(
					name=frappe.utils.get_link_to_form(doc.doctype, doc.name),
					doc_start=get_time(doc.delivery_start_time).strftime("%I:%M %p"),
					doc_end=get_time(doc.delivery_end_time).strftime("%I:%M %p"),
					customer_start=get_time(delivery_start_time).strftime("%I:%M %p"),
					customer_end=get_time(delivery_end_time).strftime("%I:%M %p"),
				))

			frappe.sendmail(recipients=recipients, subject=subject, message=message)


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
def update_timesheet_logs(ref_dt, ref_dn, billable):
	time_logs = []

	if ref_dt in ["Project", "Task"]:
		if ref_dt == "Project":
			tasks = update_linked_tasks(ref_dn, billable)
			time_logs = [get_task_time_logs(task) for task in tasks]
			# flatten the list of time log lists
			time_logs = [log for time_log in time_logs for log in time_log]
		else:
			time_logs = frappe.get_all("Timesheet Detail", filters={frappe.scrub(ref_dt): ref_dn})

	elif ref_dt in ["Project Type", "Project Template"]:
		projects = update_linked_projects(frappe.scrub(ref_dt), ref_dn, billable)
		time_logs = [get_project_time_logs(project) for project in projects]
		# flatten the list of time log lists
		time_logs = [log for time_log in time_logs for log in time_log]

	for log in time_logs:
		frappe.db.set_value("Timesheet Detail", log.name, "billable", billable)


def update_linked_projects(ref_field, ref_value, billable):
	projects = frappe.get_all("Project", filters={ref_field: ref_value})

	for project in projects:
		project_doc = frappe.get_doc("Project", project.name)
		project_doc.billable = billable
		project_doc.save()
		update_linked_tasks(project.name, billable)

	return projects


def update_linked_tasks(project, billable):
	tasks = frappe.get_all("Task", filters={"project": project})

	for task in tasks:
		task_doc = frappe.get_doc("Task", task.name)
		task_doc.billable = billable
		task_doc.save()

	return tasks


def get_project_time_logs(project):
	return frappe.get_all("Timesheet Detail", filters={"project": project.name})

def get_task_time_logs(task):
	return frappe.get_all("Timesheet Detail", filters={"task": task.name})


@frappe.whitelist()
def get_linked_documents(doctype, name, docs=None):
	"""
	Get all nested task, timesheet and project linked doctype linkinfo

	Arguments:
		doctype (str) - The doctype for which get all linked doctypes
		name (str) - The docname for which get all linked doctypes

	Keyword Arguments:
		docs (list of dict; optional) Existing list of linked doctypes

	Returns:
		dict - Return list of documents and link count
	"""

	if not docs:
		docs = []

	linkinfo = get_linked_doctypes(doctype)
	linked_docs = get_linked_docs(doctype, name, linkinfo)
	link_count = 0
	for link_doctype, link_names in linked_docs.items():
		for link in link_names:
			docinfo = link.update({"doctype": link_doctype})
			validated_doc = validate_linked_doc(docinfo)

			if not validated_doc:
				continue

			link_count += 1
			if link.name in [doc.get("name") for doc in docs]:
				continue

			links = get_linked_documents(link_doctype, link.name, docs)
			docs.append({
				"doctype": link_doctype,
				"name": link.name,
				"docstatus": link.docstatus,
				"link_count": links.get("count")
			})

	# sort linked documents by ascending number of links
	docs.sort(key=lambda doc: doc.get("link_count"))
	return {
		"docs": docs,
		"count": link_count
	}


def validate_linked_doc(docinfo):
	# Allowed only Task, Timesheet and Project
	if docinfo.get('doctype') in ["Project", "Timesheet", "Task"]:
		return True

	return False
