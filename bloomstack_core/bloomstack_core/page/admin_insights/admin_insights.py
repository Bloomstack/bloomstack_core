import frappe


@frappe.whitelist(allow_guest=True)
def get_cubejs_host(cube_js_name="cubejs"):
    doc=frappe.get_doc("Cubejs",{"cube_js_name":cube_js_name})
    return doc