import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt


def update_order_package_tag(pick_list, method):
	package_tags = [item.package_tag for item in pick_list.locations if item.package_tag]
	if not package_tags:
		return

	for item in pick_list.locations:
		if not item.package_tag:
			continue

		if item.sales_order_item:
			existing_package_tag = frappe.db.get_value("Sales Order Item", item.sales_order_item, "package_tag")

			if method == "on_submit":
				if not existing_package_tag:
					frappe.db.set_value("Sales Order Item", item.sales_order_item, "package_tag", item.package_tag)
			elif method == "on_cancel":
				if existing_package_tag:
					frappe.db.set_value("Sales Order Item", item.sales_order_item, "package_tag", None)


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


@frappe.whitelist()
def create_pick_list(source_name, target_doc=None):
	def update_item_quantity(source, target, source_parent):
		target.qty = flt(source.qty) - flt(source.delivered_qty)
		target.stock_qty = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.conversion_factor)

	doc = get_mapped_doc('Sales Order', source_name, {
		'Sales Order': {
			'doctype': 'Pick List',
			'validation': {
				'docstatus': ['=', 1]
			}
		},
		'Sales Order Item': {
			'doctype': 'Pick List Item',
			'field_map': {
				'parent': 'sales_order',
				'name': 'sales_order_item'
			},
			'postprocess': update_item_quantity,
			'condition': lambda doc: abs(doc.delivered_qty) < abs(doc.qty) and doc.delivered_by_supplier != 1
		},
	}, target_doc)

	doc.purpose = 'Delivery against Sales Order'
	return doc
