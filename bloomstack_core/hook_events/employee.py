import frappe


def update_driver_employee(employee, method):
	if method == "validate":
		user_id = employee.user_id
		if user_id:
			driver = frappe.db.get_value("Driver", {"user_id": user_id}, "name")
		else:
			driver = frappe.db.get_value("Driver", {"employee": employee.name}, "name")

		if driver:
			frappe.db.set_value("Driver", driver, "employee", employee.name if user_id else None)
