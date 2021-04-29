import frappe

@frappe.whitelist()
def create_purchase_receipt(transfer):
	transfer = frappe.parse_json(transfer)

	for item in transfer.get("items", []):
		item =  frappe.db.get_all(("Item Supplier", filters={"supplier_part_no": item.get("product_name")}, fields = ["parent"])
		item.update({
			"item_code"	: item.parent,
			"metrc_product_name": item.get("product_name")
		})

	doc = frappe.get_doc({"doctype": "Purchase Receipt"})
	doc.update(transfer)
	doc.flags.ignore_validate=True
	doc.flags.ignore_mandatory=True
	doc.flags.ignore_links=True
	doc.insert()
