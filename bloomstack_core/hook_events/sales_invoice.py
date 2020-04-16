# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import json
from frappe.utils import get_url


def set_invoice_status(sales_invoice, method):
	sales_invoice.set_status()
	sales_invoice.set_indicator()

@frappe.whitelist()
def get_contact(name, doctype):
	out = frappe._dict()

	customer_name = frappe.db.get_value(doctype, name, ['Customer'])

	contact_persons = frappe.db.sql(
		"""
			SELECT parent,
				(SELECT is_primary_contact FROM tabContact c WHERE c.name = dl.parent) AS is_primary_contact
			FROM
				`tabDynamic Link` dl
			WHERE
				dl.link_doctype="Customer"
				AND dl.link_name=%s
				AND dl.parenttype = "Contact"
		""", (customer_name), as_dict=1)

	if contact_persons:
		for out.contact_person in contact_persons:
			out.contact_person.email_id = frappe.db.get_value("Contact", out.contact_person.parent, ["email_id"])
			if out.contact_person.is_primary_contact:
				return out

		out.contact_person = contact_persons[0]

		return out

@frappe.whitelist()
def get_attach_link(docs, doctype):
	docs = json.loads(docs)
	print_format = "print_format"
	links = []
	for doc in docs:
		link = frappe.get_template("templates/emails/print_link.html").render({
			"url": get_url(),
			"doctype": doctype,
			"name": doc.get("name"),
			"print_format": print_format,
			"key": frappe.get_doc(doctype, doc.get("name")).get_signature()
		})
		links.append(link)
	return links