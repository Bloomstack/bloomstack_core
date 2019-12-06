import frappe


def execute():
    frappe.reload_doc("hr", "doctype", "driver")
    drivers = frappe.get_all("Driver", filters={"employee": ["!=", ""]}, fields=["name", "employee"])
    
    for driver in drivers: 
        user_id = frappe.db.get_value("Employee", driver.employee, "user_id")
        if user_id:
            frappe.db.set_value("Driver", driver.name, "user_id", user_id, update_modified=False)
