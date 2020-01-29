import frappe

def execute():
    frappe.db.sql("""UPDATE 
                `tabDocType` 
            SET 
                quick_entry = 0
            WHERE 
                quick_entry = 1""")