import frappe
import json

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
	package_tag_name = []
	for item in pr.items:
		package_tag_name.append(item.package_tag)

	if len(package_tag_name) == len(set(package_tag_name)):
		for item in pr.items:
			if item.package_tag:
				package_tag = frappe.db.exists("Package Tag", {"package_tag": item.package_tag})
				if package_tag:
					frappe.throw("Package Tag already Exist")
				else:
					doc = frappe.new_doc("Package Tag")
					doc.update({
						"package_tag": item.package_tag,
						"item_code": item.item_code
					})
					doc.save()
	else:
		frappe.throw("Package Tag cannot be same for multiple Purchase Receipt Item")
