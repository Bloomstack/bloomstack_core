import frappe

@frappe.whitelist()
def create_purchase_receipt(transfer):
	transfer = frappe.parse_json(transfer)

	for item in transfer.get("items", []):
		item_exists = frappe.get_all("Item", filters={"metrc_item_name": item.pop("product_name")}, fields=["name", "item_name"])
		if item_exists:
			item.update({
				"item_code": item_exists[0].name,
				"item_name": item_exists[0].item_name
			})

	doc = frappe.get_doc({"doctype": "Purchase Receipt"})
	doc.update(transfer)
	doc.flags.ignore_validate=True
	doc.flags.ignore_mandatory=True
	doc.flags.ignore_links=True
	doc.insert()
