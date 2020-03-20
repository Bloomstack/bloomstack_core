import frappe
from frappe.modules.utils import sync_customizations


def execute():
	frappe.reload_doc('bloomstack_core', 'doctype', frappe.scrub('Package Tag'))
	sync_customizations("bloomstack_core")

	doctypes = ["Batch", "Purchase Receipt Item", "Stock Entry Detail"]

	for doctype in doctypes:
		item_code_field = "item" if doctype == "Batch" else "item_code"

		packages = frappe.get_all(doctype,
			filters={"package_tag": ["!=", ""]},
			fields=["package_tag", item_code_field, "item_name"],
			distinct=1)

		for package in packages:
			package_doc = frappe.new_doc("Package Tag")
			package_doc.update({
				"package_tag": package.package_tag,
				"item_code": package.get(item_code_field),
				"item_name": package.item_name
			})

			try:
				package_doc.insert()
			except frappe.DuplicateEntryError:
				continue
