import json

import frappe
from erpnext import get_default_company
from erpnext.selling.doctype.quotation.quotation import make_sales_order
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import add_days, getdate, now
from frappe.utils.jinja import render_template

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
