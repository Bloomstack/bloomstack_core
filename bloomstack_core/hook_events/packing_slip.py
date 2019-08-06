import frappe
from frappe.model.mapper import get_mapped_doc


def create_stock_entry(packing_slip_doc, method, target_doc = None):
	def set_missing_values(source, target):
		target.purpose = "Material Transfer"
		target.company = frappe.db.get_value("Delivery Note", source.delivery_note, "company")
		packing_warehouse = frappe.db.get_single_value("Delivery Settings", "packing_warehouse")

		for item in target.items:
			if not item.t_warehouse:
				item.t_warehouse = packing_warehouse

	doc = get_mapped_doc("Packing Slip", packing_slip_doc.name, {
		"Packing Slip": {
			"doctype": "Stock Entry",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Packing Slip Item": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				"serial_no": "serial_no",
				"batch_no": "batch_no",
				"source_warehouse": "s_warehouse",
				"target_warehouse": "t_warehouse"
			},
		}
	}, target_doc, set_missing_values)
	doc.save()
	doc.submit()
