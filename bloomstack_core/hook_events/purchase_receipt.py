import frappe


def set_package_tags(pr, method):
	for item in pr.items:
		if item.batch_no and item.package_tag:
			frappe.db.set_value("Batch", item.batch_no, "package_tag", item.package_tag)
