import json

import frappe
from bloomstack_core.utils import get_abbr
from erpnext import get_default_company
from erpnext.accounts.utils import get_company_default
from frappe.utils import cstr

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

	if not frappe.db.get_single_value("Stock Settings", "autoname_item"):
		return

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

	if count > 0:
		item_code = "-".join([item_code, cstr(count+1)])
	
	# Set item document name
	item.name = item.item_code = item_code

	if not method:
		return item.item_code

def get_data(data):
	print("==========================data========================", data)
	for transaction in data.transactions:
		if transaction.get("label") == "Traceability":
			transaction.get("items", []).append("Compliance Item")

	return data
