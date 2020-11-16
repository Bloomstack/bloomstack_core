import frappe


@frappe.whitelist()
def get_cubejs_host():
    print("function is calling from home")
    return {
    "cube_js_host":frappe.conf.cube_js_host,
    "cube_js_secret":frappe.conf.cube_js_secret
    }
