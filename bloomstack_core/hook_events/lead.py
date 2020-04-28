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

def rearrange_standard_fields():
	"""Rearrange standard field in lead doctype"""
	count = 1
	for df in frappe.get_meta("Lead").get("fields"):
		if df.fieldname in ["territory", "address_html", "contact_html", "contact_by"]:
			count= count + 1
			frappe.db.sql("""UPDATE `tabDocField` SET idx={0} WHERE fieldname=%s and parent='Lead' """.format(count), df.fieldname, as_dict=True)
