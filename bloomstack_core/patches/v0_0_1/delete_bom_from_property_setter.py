import frappe

def execute():
    # Delete BOM property from property setter.
    frappe.db.sql("""DELETE FROM `tabProperty Setter`
    WHERE
    doc_type='BOM' AND property='title_field'""")
