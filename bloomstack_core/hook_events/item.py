import json

from six import string_types

import frappe
from erpnext import get_default_company
from erpnext.accounts.utils import get_company_default


@frappe.whitelist()
def autoname_item(item):
	item = frappe._dict(json.loads(item))
	item_code = autoname(item)

	return item_code


def autoname(item, method=None):
	"""
		Item Code = a + b + c + d + e, where
			a = abbreviated Company; all caps.
			b = abbreviated Brand; all caps.
			c = abbreviated Item Group; all caps.
			d = abbreviated Item Name; all caps.
			e = variant ID number; has to be incremented.
	"""

	# Get abbreviations
	company_abbr = get_company_default(get_default_company(), "abbr")
	brand_abbr = get_abbr(item.brand, max_length=len(company_abbr))
	brand_abbr = brand_abbr if company_abbr != brand_abbr else None
	item_group_abbr = get_abbr(item.item_group)
	item_name_abbr = get_abbr(item.item_name, 3)

	params = list(filter(None, [company_abbr, brand_abbr, item_group_abbr, item_name_abbr]))
	item_code = "-".join(params)

	# Get count
	count = len(frappe.get_all("Item", filters={"name": ["like", "%{}%".format(item_code)]}))
	count = "{:04d}".format(count + 1)

	# Set item document name
	item_code = "-".join([item_code, count])
	item.name = item.item_code = item_code

	return item_code


def get_abbr(txt, max_length=2):
	if not isinstance(txt, string_types):
		return

	abbr = ""
	words = txt.split(" ")

	if len(words) > 1:
		# Use initials for multi-word texts
		for word in words:
			if len(abbr) >= max_length:
				break

			if word.strip():
				abbr += word.strip()[0]
	else:
		# Use letters (upto max length) in the given string
		abbr = txt[:max_length]

	abbr = abbr.upper()
	return abbr
