import frappe
from erpnext.selling.doctype.quotation.quotation import make_sales_order
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import add_days, getdate, now


def create_project_against_contract(contract, method):
	if contract.project:
		return

	if not contract.project_template:
		return

	if not contract.is_signed:
		return

	# Get the tasks for the project
	project_tasks = []
	base_date = getdate(now())
	project_template = frappe.get_doc("Project Template", contract.project_template)

	for task in project_template.tasks:
		project_tasks.append({
			"title": task.task_name,
			"start_date": add_days(base_date, task.days_to_task_start),
			"end_date": add_days(base_date, task.days_to_task_end),
			"task_weight": task.weight,
			"description": task.description
		})

	# Get project and party details
	project_name = "{} - {}".format(contract.party_name, project_template.template_name)
	if frappe.db.exists("Project", project_name):
		count = len(frappe.get_all("Project", filters={"name": ["like", "%{}%".format(project_name)]}))
		project_name = "{} - {}".format(project_name, count)

	expected_start_date = min([task.get("start_date") for task in project_tasks if task.get("start_date")])
	expected_end_date = max([task.get("end_date") for task in project_tasks if task.get("end_date")])

	project = frappe.new_doc("Project")
	project.update({
		"project_name": project_name,
		"expected_start_date": expected_start_date,
		"expected_end_date": expected_end_date,
		"customer": contract.party_name if contract.party_type == "Customer" else None,
		"tasks": project_tasks
	})
	project.insert(ignore_permissions=True)

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


def update_status_for_contracts():
	"""
		Daily scheduler event to verify and update contract status
	"""

	contracts = frappe.get_all("Contract", filters={"docstatus": 1})

	for contract in contracts:
		contract_doc = frappe.get_doc("Contract", contract.name)

		current_statuses = (contract_doc.status, contract_doc.fulfilment_status)

		contract_doc.update_fulfilment_status()
		contract_doc.update_contract_status()

		if current_statuses != (contract_doc.status, contract_doc.fulfilment_status):
			contract_doc.save(ignore_permissions=True)
