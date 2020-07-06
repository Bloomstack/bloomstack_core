import frappe
from frappe.modules.utils import sync_customizations


def execute():
	sync_customizations("bloomstack_core")
	batches = frappe.get_all("Batch" , fields=["name", "item"])

	for batch in batches:
		item_group = frappe.db.get_value("Item", batch.item, "item_group")
		frappe.db.set_value("Batch", batch.name, "item_group", item_group, update_modified=False)