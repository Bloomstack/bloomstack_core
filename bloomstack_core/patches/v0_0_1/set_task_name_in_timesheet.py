import frappe
from frappe.modules.utils import sync_customizations


def execute():
	sync_customizations("bloomstack_core")
	timesheets = frappe.get_all("Timesheet Detail" , fields=["name", "task"])

	for timesheet in timesheets:
		task_name = frappe.db.get_value("Task", timesheet.task, "subject")
		frappe.db.set_value("Timesheet Detail", timesheet.name, "task_name", task_name, update_modified=False)