import frappe
from bloomstack_core.bloomtrace import make_integration_request

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

def create_package_from_stock(stock_entry, method):
	# TODO: Handle non-manufacture Stock Entries for intermediate packages
	stock_entry_purpose = frappe.db.get_value("Stock Entry Type", stock_entry.stock_entry_type, "purpose")
	if stock_entry_purpose not in ["Manufacture", "Repack"]:
		return

	make_integration_request("Stock Entry", stock_entry.name)