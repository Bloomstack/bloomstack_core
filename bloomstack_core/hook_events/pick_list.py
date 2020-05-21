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
