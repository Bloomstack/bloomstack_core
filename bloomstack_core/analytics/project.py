import json

import frappe

@frappe.whitelist()
def get_projects_details():
    '''Get all projects details'''
    # return  frappe.db.get_all("Project", fields=['*'])
    projects = []

    data = frappe.db.get_all("Project", fields=["*"])

    for project in data:
        open_task = frappe.db.count('Task', filters={"project":project.name,"status":"open"})
        closed_task = frappe.db.count('Task', filters={"project":project.name,"status":"completed"})
        assigned = frappe.db.get_list("ToDo", filters={"reference_type":"Project","reference_name":project.name}, fields=["*"])
        projects.append({
            "name": project.name,
            "openTask": open_task,
            "closedTasks": closed_task,
            "percentCompleted": project.percent_complete,
            "priority": project.priority,
            "assignd":assigned
        })

    return projects