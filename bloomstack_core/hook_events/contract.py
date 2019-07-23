import frappe
from frappe import _
from frappe.utils import add_days, getdate, now


def create_project_against_contract(contract, method):
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
			"start_date": add_days(base_date, task.days_to_task_start) if task.days_to_task_start else None,
			"end_date": add_days(base_date, task.days_to_task_end) if task.days_to_task_end else None,
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
	project.insert()

	# Link the contract with the project
	contract.project = project.name
