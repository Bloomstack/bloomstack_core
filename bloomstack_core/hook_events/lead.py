import frappe
from frappe.utils.nestedset import get_descendants_of


@frappe.whitelist()
def filter_territory(doctype, txt, searchfield, start, page_len, filters):
	"""filter territory"""

	territory_list = get_descendants_of("Territory", filters.get("region"))
	territory_list.append(filters.get("region"))

	return frappe.get_all('Territory',
		filters={
			'parent_territory': ('in', territory_list),
			'territory_name': ("like", "%{0}%".format(txt))
		},
		fields=["name"],
		as_list=1)

def rearrange_lead_dashboard():
	"""Rearrange standard field in lead doctype"""

	frappe.db.sql("""UPDATE `tabDocField` SET idx=2 WHERE fieldname='territory' and parent='Lead'""")
	frappe.db.sql("""UPDATE `tabDocField` SET idx=3 WHERE fieldname='address_html' and parent='Lead'""")
	frappe.db.sql("""UPDATE `tabDocField` SET idx=4 WHERE fieldname='contact_by' and parent='Lead'""")
	frappe.db.sql("""UPDATE `tabDocField` SET idx=7 WHERE fieldname='contact_html' and parent='Lead'""")
	
	
