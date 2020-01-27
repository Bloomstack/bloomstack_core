import frappe

def execute():
    doctypes = frappe.db.get_all('DocType', filters={'quick_entry': 1}, fields=['name'])
    
    for doctype in doctypes: 
        frappe.db.set_value('DocType', doctype.name, 'quick_entry', 0)
