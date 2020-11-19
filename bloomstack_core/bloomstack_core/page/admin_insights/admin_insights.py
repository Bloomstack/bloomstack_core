import frappe
from frappe.utils import get_site_name
from frappe.installer import update_site_config


@frappe.whitelist(allow_guest=True)
def get_cubejs_host(cube_js_name="bloomstack_core"):
    doc=frappe.get_doc("Cubejs",{"cube_js_name":cube_js_name})
    return doc