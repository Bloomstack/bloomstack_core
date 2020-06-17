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
		package_tag_list = []
		for i in range(len(package_tags)):
			k = i + 1
			for j in range(k, len(package_tags)):
				if package_tags[i] == package_tags[j] and package_tags[i] not in package_tag_list:
					package_tag_list.append(package_tags[i])
		frappe.throw("Package Tag {0} cannot be same for multiple Purchase Receipt Item".format(", ".join(package_tag_list)))

	for item in pr.items:
		if item.package_tag:
			package_tag = frappe.db.exists("Package Tag", {"package_tag": item.package_tag})
			if package_tag:
				frappe.throw("Package Tag {0} already Exist".format(package_tag))
			else:
				doc = frappe.new_doc("Package Tag")
				doc.update({
					"package_tag": item.package_tag,
					"item_code": item.item_code
				})
				doc.save()
