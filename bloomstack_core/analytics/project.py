import json

import frappe
from frappe.sessions import Session, clear_sessions, delete_session

@frappe.whitelist()
def get_logged_user():
	return frappe.session.user

@frappe.whitelist()
def get_projects_details():
    '''Get all projects details'''
    # return  frappe.db.get_all("Project", fields=['*'])
    projects = []

    data = frappe.db.get_all("Project", fields=["name","percent_complete","priority","_assign"])

    for project in data:
        projects.append({
            "name": project.name,
            "percentCompleted": project.percent_complete,
            "priority": project.priority,
            "assignd":project._assign
        })

    return projects