import frappe


def update_package_tags(pr, method):
	for item in pr.items:
		if item.batch_no and item.package_tag:
			if method == "on_submit":
				frappe.db.set_value("Package Tag", item.package_tag, "item_code", item.item_code)
				frappe.db.set_value("Package Tag", item.package_tag, "batch_no", item.batch_no)
			elif method == "before_cancel":
				frappe.db.set_value("Package Tag", item.package_tag, "item_code", None)
				frappe.db.set_value("Package Tag", item.package_tag, "item_name", None)
				frappe.db.set_value("Package Tag", item.package_tag, "item_group", None)
				frappe.db.set_value("Package Tag", item.package_tag, "batch_no", None)
