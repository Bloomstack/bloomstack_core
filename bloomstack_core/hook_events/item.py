from six import string_types

import frappe
from erpnext import get_default_company
from erpnext.accounts.utils import get_company_default


def autoname(item, method):
	"""
		Item Code = a + b + c + d + e, where
			a = abbreviated Company; first 3 letters - all caps.
			b = abbreviated Brand; first 2 letters - all caps.
			c = abbreviated Item Group; first 2 letters - all caps.
			d = abbreviated Item Name; first 3 letters - all caps.
			e = variant ID number; has to be incremented.
	"""

	# Get abbreviations
	company_abbr = get_company_default(get_default_company(), "abbr")
	brand_abbr = get_abbr(item.brand)
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


def get_abbr(txt, max_length=2):
	from six import string_types
	abbr = ""

	if not isinstance(txt, string_types):
		return abbr

	words = txt.split(" ")
	if len(words) > 1:
		# Use initials for multi-word texts
		for word in words:
			if len(abbr) >= max_length:
				return abbr

			if word.strip():
				abbr += word.strip()[0]
	else:
		# Use letters (upto max length) in the given string
		abbr = txt[:max_length]

	abbr = abbr.upper()
	return abbr
