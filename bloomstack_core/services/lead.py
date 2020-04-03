import json

import frappe
from frappe.utils.nestedset import get_descendants_of

@frappe.whitelist()
def filter_territory(doctype, txt, searchfield, start, page_len, filters):
	"""filter territory"""

	company_list = get_descendants_of("Territory", filters.get("region"))                            
	company_list.append(filters.get("region"))

	return frappe.db.get_all("Territory", filters=[dict(parent_territory = ('in', company_list))], fields=['name'], as_list=1)