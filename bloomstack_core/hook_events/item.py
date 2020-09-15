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
