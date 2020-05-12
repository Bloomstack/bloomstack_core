# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import json
import frappe
from frappe.utils import nowdate
from frappe.utils.nestedset import get_root_of


@frappe.whitelist()
def get_items(start, page_length, price_list, item_group, search_value=""	):
	data = dict()

	if not frappe.db.exists('Item Group', item_group):
		item_group = get_root_of('Item Group')

	if search_value:
		data = search_serial_or_batch_or_barcode_number(search_value)

	item_code = data.get("item_code") if data.get("item_code") else search_value
	serial_no = data.get("serial_no") if data.get("serial_no") else ""
	batch_no = data.get("batch_no") if data.get("batch_no") else ""
	barcode = data.get("barcode") if data.get("barcode") else ""

	condition = get_conditions(item_code, serial_no, batch_no, barcode)

	lft, rgt = frappe.db.get_value('Item Group', item_group, ['lft', 'rgt'])
	# locate function is used to sort by closest match from the beginning of the value


	result = []

	items_data = frappe.db.sql(""" SELECT
			item.name as item_code,
			item.stock_uom as stock_uom,
			item.item_name as item_name,
			item.image as item_image,
			item.idx as idx,
			item.is_stock_item as is_stock_item,
			item.item_group as item_group,
			item.has_batch_no as has_batch_no
		FROM
			`tabItem` item
		WHERE
			disabled = 0 and has_variants = 0 and is_sales_item = 1
			and item_group in (select name from `tabItem Group` where lft >= {lft} and rgt <= {rgt})
			and {condition} order by idx desc limit {start}, {page_length}"""
		.format(
			start=start, page_length=page_length,
			lft=lft, rgt=rgt,
			condition=condition
		), as_dict=1)

	if items_data:
		items = [d.item_code for d in items_data]
		item_prices_data = frappe.get_all("Item Price",
			fields = ["item_code", "price_list_rate", "currency"],
			filters = {'price_list': price_list, 'item_code': ['in', items]})

		item_warehouse_list = frappe.get_all("Item Default",
			fields = ["parent", "default_warehouse"],
			filters = {'parent': ['in', items]})

		warehouses = {}
		for warehouse in item_warehouse_list:
			warehouses[warehouse.parent] = warehouse.default_warehouse

		item_prices = {}
		for d in item_prices_data:
			item_prices[d.item_code] = d

		# update below get stock from Bin with a group query & joins to optimize performance.
		for item in items_data:
			row = {}
			actual_qty = 0

			actual_qty =  frappe.get_all('Bin', fields=['sum(actual_qty) as actual_qty'],
				filters={ 'item_code' : item.item_code, 'warehouse': warehouses.get(item.item_code) }
			)[0].get("actual_qty")

			row.update(item)
			item_price = item_prices.get(item.item_code) or {}
			row.update({
				'price_list_rate': item_price.get('price_list_rate'),
				'currency': item_price.get('currency'),
				'default_warehouse': warehouses.get(item.item_code),
				'actual_qty': actual_qty
			})
			result.append(row)

	res = {
		'items': result
	}

	if serial_no:
		res.update({
			'serial_no': serial_no
		})

	if batch_no:
		res.update({
			'batch_no': batch_no
		})

	if barcode:
		res.update({
			'barcode': barcode
		})

	return res

@frappe.whitelist()
def search_serial_or_batch_or_barcode_number(search_value):
	# search barcode no
	barcode = frappe.db.get_value('Item Barcode', {'barcode': search_value}, ['barcode', 'parent as item_code'], as_dict=True)
	if barcode:
		return barcode

	# search serial no
	serial_no = frappe.get_all('Serial No',
		{"name": search_value, "warranty_expiry_date": ["<=", nowdate()], "amc_expiry_date": ["<=", nowdate()]},
		['name as serial_no', 'item_code'])
	if serial_no:
		return serial_no[0]

	# search batch no
	batch_no = frappe.get_all('Batch',
		{"name": search_value, "batch_qty": [">", 0], "disabled": 0, "expiry_date": ["<=", nowdate()]},
		['name as batch_no', 'item as item_code'])
	if batch_no:
		return batch_no[0]

	return {}

def get_conditions(item_code, serial_no, batch_no, barcode):
	if serial_no or batch_no or barcode:
		return "name = {0}".format(frappe.db.escape(item_code))

	return """(name like {item_code}
		or item_name like {item_code})""".format(item_code = frappe.db.escape('%' + item_code + '%'))

def item_group_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(""" select distinct name from `tabItem Group`
			where (name like %(txt)s) limit {start}, {page_len}"""
		.format(start=start, page_len= page_len),
			{'txt': '%%%s%%' % txt})
