import frappe


def add_comment_to_batch(stock_entry, method):
	for item in stock_entry.items:
		if item.batch_no:
			if item.s_warehouse:
				comment_text = "{qty} {uom} consumed by {stock_entry}".format(
					qty=item.qty, uom=item.uom, stock_entry=stock_entry.name)
			elif item.t_warehouse:
				comment_text = "{qty} {uom} created from {stock_entry}".format(
					qty=item.qty, uom=item.uom, stock_entry=stock_entry.name)

			batch_doc = frappe.get_doc("Batch", item.batch_no)
			comment = batch_doc.add_comment(comment_type="Comment", text=comment_text)
			comment.comment_type = "Info"
			comment.save()

	frappe.db.commit()

def update_coa_batch_no(stock_entry, method):
	stock_entry_purpose = frappe.db.get_value("Stock Entry Type", stock_entry.stock_entry_type, "purpose")
	if stock_entry_purpose == "Material Receipt":
		for item in stock_entry.items:
			if item.package_tag:
				frappe.db.set_value("Package Tag", item.package_tag, "coa_batch_no", item.batch_no)
	elif stock_entry_purpose in ["Manufacture", "Repack"]:
		source_item =  next((item for item in stock_entry.items if item.s_warehouse), None)
		for item in stock_entry.items:
			if item.package_tag and item.t_warehouse:
				if frappe.db.get_value("Item", item.item_code, "requires_lab_tests"):
					frappe.db.set_value("Package Tag", item.package_tag, "coa_batch_no", item.batch_no)
				else:
					coa_batch_no = frappe.db.get_value("Package Tag", source_item.package_tag, "coa_batch_no")
					frappe.db.set_value("Package Tag", item.package_tag, "coa_batch_no", coa_batch_no)