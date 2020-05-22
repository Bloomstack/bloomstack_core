import frappe


def execute():
	frappe.reload_doc("bloomstack_core", "doctype", "package_tag")

	batches_with_package_tags = frappe.get_all("Batch",
		filters={"package_tag": ["is", "set"]},
		fields=["name", "package_tag"])

	for batch in batches_with_package_tags:
		frappe.db.set_value("Package Tag", batch.package_tag, "batch_no", batch.name)
