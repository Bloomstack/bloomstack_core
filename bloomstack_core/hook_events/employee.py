from __future__ import unicode_literals
import frappe
from frappe import _

def update_driver_employee(employee, method):
	if method == "validate":
		user_id = employee.user_id
		if user_id:
			driver = frappe.db.get_value("Driver", {"user_id": user_id}, "name")
		else:
			driver = frappe.db.get_value("Driver", {"employee": employee.name}, "name")

		if driver:
			frappe.db.set_value("Driver", driver, "employee", employee.name if user_id else None)

def get_data(data):
	return frappe._dict({
		'heatmap': True,
		'heatmap_message': _('This is based on the attendance of this Employee'),
		'fieldname': 'employee',
		'transactions': [
			{
				'label': _('Leave and Attendance'),
				'items': ['Attendance', 'Attendance Request', 'Leave Application', 'Leave Allocation', 'Employee Checkin']
			},
			{
				'label': _('Lifecycle'),
				'items': ['Employee Transfer', 'Employee Promotion', 'Employee Separation']
			},
			{
				'label': _('Shift'),
				'items': ['Shift Request', 'Shift Assignment']
			},
			{
				'label': _('Expense'),
				'items': ['Expense Claim', 'Travel Request', 'Employee Advance']
			},
			{
				'label': _('Benefit'),
				'items': ['Employee Benefit Application', 'Employee Benefit Claim' ,'Employee Compensation']
			},
			{
				'label': _('Evaluation'),
				'items': ['Appraisal']
			},
			{
				'label': _('Payroll'),
				'items': ['Salary Structure Assignment', 'Salary Slip', 'Additional Salary', 'Timesheet','Employee Incentive', 'Retention Bonus']
			},
			{
				'label': _('Training'),
				'items': ['Training Event', 'Training Result', 'Training Feedback', 'Employee Skill Map']
			},
		]
	})