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

def create_package_tag(pr, method):
	package_tags = [item.package_tag for item in pr.items if item.package_tag]

	if len(package_tags) != len(set(package_tags)):
		duplicate_tags = list(set([tag for tag in package_tags if package_tags.count(tag) > 1]))
		frappe.throw("Package Tag {0} cannot be same for multiple Purchase Receipt Item".format(", ".join(duplicate_tags)))

	for item in pr.items:
		if item.package_tag:
			package_tag = frappe.db.exists("Package Tag", {"package_tag": item.package_tag})
			if package_tag:
				frappe.throw("Row #{0}: Package Tag '{1}' already exists".format(item.idx, frappe.utils.get_link_to_form("Package Tag", package_tag)))
			else:
				doc = frappe.new_doc("Package Tag")
				doc.update({
					"package_tag": item.package_tag,
					"item_code": item.item_code
				})
				doc.save()
