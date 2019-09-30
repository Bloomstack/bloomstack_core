import json

import frappe


@frappe.whitelist()
def set_roles():
	"""overrides roles for a user"""
	data = json.loads(frappe.request.data)
	user = frappe.get_doc("User", data.get("uid"))
	user.set("roles", list(set(d for d in user.get("roles") if d.role in data.get("roles"))))
	user.add_roles(*data.get("roles"))
