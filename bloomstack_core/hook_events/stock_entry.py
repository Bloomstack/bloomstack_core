import frappe
from frappe.utils import getdate, add_days, today, now_datetime, get_date_str

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

def raw_material_update_on_bom():
	past_seven_days = get_date_str(add_days(today(), -7))
	todays_date = today()
	boms = frappe.get_all("BOM", filters= {
		"manufacturing_type" : "Process"
	},
	fields=["name"]
	)
	for bom in boms:
		stocks = frappe.get_all("Stock Entry", filters={
			"bom_no": bom.name,
			"posting_date": ["BETWEEN", [past_seven_days, todays_date]]
		})
		raw_material = 0
		fg= 0
		avg_manufactured_qty = 0
		for stock in stocks:
			stock_entry = frappe.get_doc("Stock Entry", {"name": stock.name, "bom_no": bom.name})
			for item in stock_entry.items:
				if item.s_warehouse:
					raw_material = raw_material + item.qty
				elif item.t_warehouse:
					fg = fg + item.qty
		if fg and raw_material:
			avg_manufactured_qty= fg/raw_material
		frappe.db.set_value("BOM", bom.name, "avg_manufactured_qty", avg_manufactured_qty)
