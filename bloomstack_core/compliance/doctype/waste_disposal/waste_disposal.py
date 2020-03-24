# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import json

import frappe
from erpnext.stock.doctype.batch.batch import get_batch_qty
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class WasteDisposal(Document):
	pass


@frappe.whitelist()
def create_stock_entry_for_waste_disposal(doc):
	if isinstance(doc, str):
		doc = frappe._dict(json.loads(doc))

	stock_entry = get_mapped_doc("Waste Disposal", doc.name, {
		"Waste Disposal": {
			"doctype": "Stock Entry"
		},
		"Waste Disposal Item": {
			"doctype": "Stock Entry Detail",
			"field_map": {
				"warehouse": "s_warehouse",
				"batch_no": "batch_no",
				"serial_no": "serial_no"
			}
		}
	})

	stock_entry.stock_entry_type = "Material Issue"
	stock_entry.save()
	stock_entry.submit()

	return stock_entry.name


@frappe.whitelist()
def get_items(warehouse, posting_date, posting_time, company):
	lft, rgt = frappe.db.get_value("Warehouse", warehouse, ["lft", "rgt"])

	items = frappe.db.sql("""
		SELECT
			i.name AS item_code,
			i.item_name AS item_name,
			bin.warehouse AS warehouse
		FROM
			tabBin bin
				JOIN tabItem i ON i.name = bin.item_code
		WHERE
			i.disabled = 0
				AND EXISTS(
					SELECT
						name
					FROM
						`tabWarehouse`
					WHERE
						lft >= %s
							AND rgt <= %s
							AND name = bin.warehouse
				)
	""", (lft, rgt), as_dict=True)

	items += frappe.db.sql("""
		SELECT
			i.name AS item_code,
			i.item_name AS item_name,
			id.default_warehouse AS warehouse
		FROM
			tabItem i
				JOIN `tabItem Default` id ON i.name = id.parent
		WHERE
			i.is_stock_item = 1
				AND i.has_serial_no = 0
				AND i.has_batch_no = 0
				AND i.has_variants = 0
				AND i.disabled = 0
				AND id.company = %s
				AND EXISTS(
					SELECT
						name
					FROM
						`tabWarehouse`
					WHERE
						lft >= %s
							AND rgt <= %s
							AND name = id.default_warehouse
				)
		GROUP BY
			i.name
	""", (lft, rgt, company), as_dict=True)

	res = []

	for item in items:
		batch_details = get_batch_qty(warehouse=item.warehouse, item_code=item.item_code) or []

		for batch in batch_details:
			if batch.qty > 0:
				res.append({
					"item_code": item.item_code,
					"warehouse": item.warehouse,
					"qty": batch.qty,
					"item_name": item.item_name,
					"current_qty": batch.qty,
					"batch_no": batch.batch_no
				})

	return res
