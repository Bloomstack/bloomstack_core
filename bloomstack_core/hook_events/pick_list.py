import frappe


def update_order_package_tag(pick_list, method):
	package_tags = [item.package_tag for item in pick_list.locations if item.package_tag]
	if not package_tags:
		return

	for item in pick_list.locations:
		if not item.package_tag:
			continue

		if item.sales_order_item:
			if method == "on_submit":
				frappe.db.set_value("Sales Order Item", item.sales_order_item, "package_tag", item.package_tag)
			elif method == "on_cancel":
				frappe.db.set_value("Sales Order Item", item.sales_order_item, "package_tag", "")


def update_package_tag(pick_list, method):
	package_tags = [item.package_tag for item in pick_list.locations if item.package_tag]
	if not package_tags:
		return

	for item in pick_list.locations:
		if not item.package_tag:
			continue

		if item.sales_order_item:
			package_tag = frappe.get_doc("Package Tag", item.package_tag)

			if method == "on_submit":
				source_package_tag = frappe.db.get_value("Sales Order Item", item.sales_order_item, "package_tag")
				source_package_tag = source_package_tag if source_package_tag != item.package_tag else None

				package_tag.update({
					"item_code": item.item_code,
					"batch_no": item.batch_no,
					"source_package_tag": source_package_tag
				})
				package_tag.save()
			elif method == "on_cancel":
				package_tag.update({
					"item_code": None,
					"item_name": None,
					"item_group": None,
					"batch_no": None,
					"source_package_tag": None
				})
				package_tag.save()
