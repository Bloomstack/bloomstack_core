import json

import frappe
from erpnext import get_default_company
from erpnext.selling.doctype.quotation.quotation import make_sales_order
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import add_days, getdate, now
from frappe.utils.jinja import render_template


def generate_contract_terms_display(contract, method):
	if contract.contract_terms:
		contract.contract_terms_display = render_template(contract.contract_terms, {"doc": contract.as_dict()})


def create_project_against_contract(contract, method):
	if contract.project:
		return

	if not contract.project_template:
		return

	if not contract.is_signed:
		return

	# Get the tasks for the project
	base_date = getdate(now())
	project_template = frappe.get_doc("Project Template", contract.project_template)

	# Get project and party details
	project_name = "{} - {}".format(contract.party_name, project_template.template_name)
	if frappe.db.exists("Project", project_name):
		count = len(frappe.get_all("Project", filters={"name": ["like", "%{}%".format(project_name)]}))
		project_name = "{} - {}".format(project_name, count)

	project = frappe.new_doc("Project")
	project.update({
		"project_name": project_name,
		"customer": contract.party_name if contract.party_type == "Customer" else None,
	})

	project.insert(ignore_permissions=True)

	project_dates = []
	project_name = project.name
	for task in project_template.tasks:
		project_task = frappe.new_doc("Task")
		start_date = add_days(base_date, task.days_to_task_start)
		end_date = add_days(base_date, task.days_to_task_end)
		project_task.update({
			"subject": task.task_name,
			"start_date": start_date,
			"end_date": end_date,
			"task_weight": task.weight,
			"description": task.description,
			"project": project_name
		})
		project_task.insert(ignore_permissions=True)
		project_dates.extend([start_date, end_date])

	expected_start_date = min(project_dates)
	expected_end_date = max(project_dates)

	project.update({
		"expected_start_date": expected_start_date,
		"expected_end_date": expected_end_date
	})

	project.save(ignore_permissions=True)


	# Link the contract with the project
	contract.db_set("project", project.name)


def create_order_against_contract(contract, method):
	if frappe.db.exists("Sales Order", {"contract": contract.name}):
		return

	if not contract.is_signed:
		return

	if contract.document_type == "Quotation" and contract.document_name:
		sales_order = make_sales_order(contract.document_name)
		sales_order.contract = contract.name
		sales_order.project = contract.project
		sales_order.delivery_date = frappe.db.get_value("Project", contract.project, "expected_end_date")
		sales_order.save()
		sales_order.submit()


def create_event_against_contract(contract, method):
	if method == "on_cancel":
		event_name = frappe.db.exists('Event', {'subject': contract.name})
		if event_name:
			frappe.delete_doc('Event', event_name)
	elif method == "on_submit":
		if not contract.end_date:
			return

		employee_id = frappe.db.get_value('Employee', {'user_id': contract.signed_by_company}, 'name')
		event = frappe.new_doc('Event')
		event.subject = contract.name
		event.ends_on = contract.end_date
		event.description = contract.contract_terms
		event.all_day = 1
		event.append("event_participants", {
			"reference_doctype": contract.party_type,
			"reference_docname": contract.party_name
		})

		if employee_id:
			event.append("event_participants", {
				"reference_doctype": 'Employee',
				"reference_docname": employee_id
			})

		event.save()


@frappe.whitelist()
def get_party_users(doctype, txt, searchfield, start, page_len, filters):
	if filters.get("party_type") in ("Customer", "Supplier"):
		party_links = frappe.get_all("Dynamic Link",
			filters={"parenttype": "Contact",
				"link_doctype": filters.get("party_type"),
				"link_name": filters.get("party_name")},
			fields=["parent"])

		party_users = [frappe.db.get_value("Contact", link.parent, "user") for link in party_links]

		return frappe.get_all("User", filters={"email": ["in", party_users]}, as_list=True)


def get_data(data):
	return frappe._dict({
		'fieldname': 'contract',
		'internal_links': {
			'Project': 'project'
		},
		'transactions': [
			{
				'label': _('Sales'),
				'items': ['Sales Order']
			},
			{
				'label': _('Projects'),
				'items': ['Project']
			}
		]
	})


def set_contract_company(contract, method):
	contract.signed_by_company = frappe.session.user
	if contract.company:
		contract.letter_head = frappe.db.get_value("Company", contract.company, "default_letter_head")

@frappe.whitelist()
def get_events(start, end, filters=None):
	"""
	Returns events for Gantt / Calendar view rendering.

	Args:
		start (str): Start date-time.
		end (str): End date-time.
		filters (str, optional): Filters (JSON). Defaults to None.

	Returns:
		list of dict: The list of Contract events
	"""

	filters = json.loads(filters)
	from frappe.desk.calendar import get_event_conditions
	conditions = get_event_conditions("Contract", filters)

	events = frappe.db.sql("""
		SELECT
			name,
			start_date,
			end_date
		FROM
			`tabContract`
		WHERE
			(start_date <= %(end)s
				AND end_date >= %(start)s)
				AND docstatus < 2
				{conditions}
		""".format(conditions=conditions), {
			"start": start,
			"end": end
		},
		as_dict=True,
		update={"allDay": 0}
	)
	return events
