import frappe
import json
import ast

@frappe.whitelist(allow_guest=True)
def get_cubejs_host(cube_js_name="cubejs"):
	doc=frappe.get_doc("Cubejs",{"cube_js_name":cube_js_name})
	return doc

@frappe.whitelist(allow_guest=True)
def get_all_insights_data(types=None):
	fetched_data = []
	if not types:
		fetched_data = frappe.db.get_list("Admin Insights", fields= ["data", "type"], order_by="type")
		return fetched_data
	datas = frappe.get_all("Admin Insights", filters={'type': ['=', types]})
	if not datas:
		return "No Data Found For Type "+ types

	for data in datas:
		fetched_data.append(json.loads(frappe.get_value("Admin Insights", data.name , ["data"])))

	print(fetched_data)
	return fetched_data

@frappe.whitelist()
def create_admin_insights(types, data_object):
	if(data_object[0]=='['):
		data_object =  ast.literal_eval(data_object)
		for data in data_object:
			doc = frappe.new_doc("Admin Insights")
			doc.type = types
			doc.data = json.dumps(data)
			print(doc)
			doc.insert()
			doc.submit()
	else:
		doc = frappe.new_doc("Admin Insights")
		doc.type = types
		doc.data = json.dumps(json.loads(data_object))
		doc.insert()
		doc.submit()
	return "The Data Is Inserted"