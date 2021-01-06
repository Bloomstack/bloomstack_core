import frappe
import json

@frappe.whitelist(allow_guest=True)
def get_cubejs_host(cube_js_name="cubejs"):
	doc=frappe.get_doc("Cubejs",{"cube_js_name":cube_js_name})
	return doc

@frappe.whitelist(allow_guest=True)
def get_all_insights_data(types=None):
	fetched_data = []
	if not types:
		fetched_data.append(frappe.db.get_list("Admin Insights", fields= ["data_object"]))
		# print("-----------------------------", fetched_data)
		return fetched_data
	datas = frappe.get_all("Admin Insights", filters={'type': ['=', types]})
	if not datas:
		return "No Data Found For Type "+ types

	for data in datas:
		fetched_data.append(json.loads(frappe.get_value("Admin Insights", data.name , ["data_object"])))

	print(fetched_data)
	return fetched_data

@frappe.whitelist()
def create_admin_insights(types, data_object):
	doc = frappe.new_doc("Admin Insights")
	doc.type = types
	doc.data_object = data_object
	doc.insert()
	doc.submit()
	return "The Data Is Inserted"