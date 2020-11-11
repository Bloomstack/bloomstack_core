import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe import _
from frappe.utils import cstr, get_host_name


def execute_bloomtrace_integration_request():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	pending_requests = frappe.get_all("Integration Request", filters={
		"status": ["IN", ["Queued", "Failed"]],
		"reference_doctype": "Item",
		"integration_request_service": "BloomTrace"
	}, order_by="creation ASC", limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		item = frappe.get_doc("Item", integration_request.reference_docname)

		try:
			if not item.bloomtrace_id:
				insert_compliance_item(item, frappe_client)
			else:
				update_compliance_item(item, frappe_client)

			integration_request.error = ""
			integration_request.status = "Completed"
		except Exception as e:
			integration_request.error = cstr(e)
			integration_request.status = "Failed"

		integration_request.save(ignore_permissions=True)


def insert_compliance_item(item, frappe_client):
	bloomtrace_compliance_item_dict = make_compliance_item(item)
	bloomtrace_compliance_item = frappe_client.insert(bloomtrace_compliance_item_dict)
	bloomtrace_id = bloomtrace_compliance_item.get('name')
	frappe.db.set_value("Item", item.name, "bloomtrace_id", bloomtrace_id)


def update_compliance_item(item, frappe_client):
	bloomtrace_compliance_item_dict = make_compliance_item(item)
	bloomtrace_compliance_item_dict.update({
		"name": item.bloomtrace_id
	})
	frappe_client.update(bloomtrace_compliance_item_dict)


def make_compliance_item(item):
	bloomtrace_compliance_item_dict = {
		"doctype": "Compliance Item",
		"bloomstack_site": get_host_name(),
		"item_code": item.item_code,
		"item_name": item.item_name,
		"enable_metrc": item.enable_metrc,
		"metrc_id": item.metrc_id,
		"metrc_item_category": item.metrc_item_category,
		"metrc_unit_value": item.metrc_unit_value,
		"metrc_uom": item.metrc_uom,
		"metrc_unit_uom": item.metrc_unit_uom
	}
	return bloomtrace_compliance_item_dict


# Search querries
def metrc_item_category_query(doctype, txt, searchfield, start, page_len, filters):
	metrc_uom = filters.get("metrc_uom")
	quantity_type = frappe.db.get_value("Compliance UOM", metrc_uom, "quantity_type")

	return frappe.get_all("Compliance Item Category", filters={"quantity_type": quantity_type}, as_list=1)


def metrc_uom_query(doctype, txt, searchfield, start, page_len, filters):
	metrc_item_category = filters.get("metrc_item_category")
	quantity_type = frappe.db.get_value("Compliance Item Category", metrc_item_category, "quantity_type")

	return frappe.get_all("Compliance UOM", filters={"quantity_type": quantity_type}, as_list=1)


def metrc_unit_uom_query(doctype, txt, searchfield, start, page_len, filters):
	metrc_item_category = filters.get("metrc_item_category")
	mandatory_unit = frappe.db.get_value("Compliance Item Category", metrc_item_category, "mandatory_unit")

	quantity_type = "VolumeBased"
	if mandatory_unit == "Weight":
		quantity_type = "WeightBased"

	return frappe.get_all("Compliance UOM", filters={"quantity_type": quantity_type}, as_list=1)
