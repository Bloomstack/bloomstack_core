import json

import frappe
from frappe.utils import get_gravatar_url, get_url_to_form


@frappe.whitelist()
def get_project_details():
	'''Get all projects details'''

	project_data = []
	projects = frappe.db.get_all("Project", fields=["name", "priority", "percent_complete", "_assign"])

	for project in projects:
		project_users = []

		total_tasks = frappe.db.count("Task", filters={"project": project.name})
		closed_tasks = frappe.db.count("Task", filters={"project": project.name, "status": "Completed"})
		assigned_users = json.loads(project._assign)

		for assignee in assigned_users:
			full_name = frappe.db.get_value("User", assignee, "full_name")
			assignee_tasks = frappe.get_list("Task",
				filters={"_assign": ["like", "%{}%".format(assignee)]},
				fields=["name", "status"])

			user_data = {
				"name": assignee,
				"label": full_name,
				"avatar": get_gravatar_url(assignee),
				"tasks": []
			}

			for task in assignee_tasks:
				user_data["tasks"].append({
					"url": get_url_to_form("Task", task.name),
					"status": task.status
				})

			project_users.append(user_data)

		project_data.append({
			"name": project.name,
			"totalTasks": total_tasks,
			"closedTasks": closed_tasks,
			"percentCompleted": project.percent_complete,
			"priority": project.priority,
			"assigned": project_users
		})

	return project_data
