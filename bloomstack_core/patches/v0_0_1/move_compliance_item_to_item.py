import frappe
from frappe.modules.utils import sync_customizations


def execute():
	compliance_items = frappe.get_all("Compliance Item", fields=["*"])

	frappe.reload_doc("stock", "doctype", "item")
	sync_customizations("bloomstack_core")

	fields = ["requires_lab_tests", "enable_cultivation_tax",
		"strain_type", "item_category", "enable_metrc",
		"metrc_id", "metrc_item_category", "metrc_unit_value",
		"metrc_uom", "metrc_unit_uom", "bloomtrace_id"]

	for item in compliance_items:
		if not item.item_code:
			continue

		frappe.db.set_value("Item", item.item_code, "is_compliance_item", True, update_modified=False)

		for field in fields:
			if item.get(field):
				frappe.db.set_value("Item", item.item_code, field, item.get(field), update_modified=False)

	frappe.delete_doc_if_exists("Custom Field", "Compliance Item-enable_metrc")
	frappe.delete_doc_if_exists("Custom Field", "Compliance Item-sb_item_details")
	frappe.delete_doc_if_exists("Custom Field", "Compliance Item-metrc_id")
	frappe.delete_doc_if_exists("Custom Field", "Compliance Item-metrc_item_category")
	frappe.delete_doc_if_exists("Custom Field", "Compliance Item-metrc_unit_value")
	frappe.delete_doc_if_exists("Custom Field", "Compliance Item-cb_item_details")
	frappe.delete_doc_if_exists("Custom Field", "Compliance Item-metrc_uom")
	frappe.delete_doc_if_exists("Custom Field", "Compliance Item-metrc_unit_uom")
	frappe.delete_doc_if_exists("Custom Field", "Compliance Item-bloomtrace_id")
