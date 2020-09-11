# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloom Stack and contributors
# For license information, please see license.txt

import frappe


def add_comment_to_batch(stock_entry, method):
	for item in stock_entry.items:
		if item.batch_no:

			comment_text = "{qty} {uom} {consumed_or_created} {stock_entry}".format(
				qty=item.qty,
				uom=item.uom,
				consumed_or_created = "consumed by" if item.s_warehouse else "created_from",
				stock_entry=stock_entry.name
			)

			frappe.get_doc({
				"doctype":"Comment",
				'comment_type': "Info",
				"comment_email": frappe.session.user,
				"reference_doctype": "Batch",
				"reference_name": item.batch_no,
				"content": comment_text,
			}).insert(ignore_permissions=True)
