from urllib.parse import urlparse

import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from bloomstack_core.compliance.utils import get_metrc, log_request
from frappe import _
from frappe.utils import cstr, get_url


def get_item(item):
	"""
	Get the METRC Item for a synced Bloomstack Item.

	Args:
		item (object): The `Item` data for fetching from METRC.

	Returns:
		dict: The METRC Item data, if it exists, otherwise `None`.
	"""
	metrc = get_metrc()

	if not metrc:
		return

	response = metrc.items.active.get()

	if not response.ok:
		frappe.throw(_("Could not fetch items from METRC. Please try again later."))

	metrc_item = next((_item for _item in response.json() if _item.get('Name') == item.item_name), None)

	return metrc_item


def create_item(item):
	"""
	Create a Bloomstack item in METRC.

	Args:
		item (object): The `Item` data to create in METRC.

	Returns:
		int: The ID of the created METRC Item, if created, otherwise `None`.
	"""

	# Create the item record on METRC
	metrc = get_metrc()

	if not metrc:
		return

	payload = build_payload(item)
	response = metrc.items.create.post(json=payload)
	log_request(response.url, payload, response, "Item", item.name)

	if not response.ok:
		frappe.throw(_(response.raise_for_status()))

	metrc_item = get_item(item)

	if metrc_item:
		return metrc_item.get("Id")


def update_item(item):
	"""
	Update a Bloomstack item in METRC.

	Args:
		item (object): The `Item` data to update in METRC.
	"""
	metrc = get_metrc()

	if not metrc:
		return

	payload = build_payload(item)
	response = metrc.items.update.post(json=payload)
	log_request(response.url, payload, response, "Item", item.name)

	if not response.ok:
		frappe.throw(_(response.raise_for_status()))


def build_payload(item):
	"""
	Create the request body for the Item endpoint.

	Args:
		item (object): The `Item` data.

	Returns:
		list of dict: The `METRC Item` payload.
	"""

	item_data = {
		"Name": item.item_name,
		"ItemCategory": item.metrc_item_category,
		"UnitOfMeasure": item.metrc_uom
	}

	if item.metrc_id:
		item_data.update({
			"Id": item.metrc_id
		})

	mandatory_metrc_unit = frappe.db.get_value("Compliance Item Category", item.metrc_item_category, "mandatory_unit")

	if mandatory_metrc_unit == "Volume":
		item_data.update({
			"UnitVolume": item.metrc_unit_value,
			"UnitVolumeUnitOfMeasure": item.metrc_unit_uom
		})
	elif mandatory_metrc_unit == "Weight":
		item_data.update({
			"UnitWeight": item.metrc_unit_value,
			"UnitWeightUnitOfMeasure": item.metrc_unit_uom
		})

	payload = [item_data]
	return payload


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

	quantity_type = None
	if mandatory_unit == "Volume":
		quantity_type = "VolumeBased"
	elif mandatory_unit == "Weight":
		quantity_type = "WeightBased"

	return frappe.get_all("Compliance UOM", filters={"quantity_type": quantity_type}, as_list=1)


def sync_metrc_item(item, method):
	if item.enable_metrc:
		if method == "validate":
			if not item.is_new():
				_sync_metrc_item(item)
		elif method == "after_insert":
			_sync_metrc_item(item)


def _sync_metrc_item(item):
	if not item.metrc_id:
		metrc_id = create_item(item)
		if metrc_id:
			frappe.db.set_value("Item", item.name, "metrc_id", metrc_id)
			frappe.msgprint(_("{} was successfully created in METRC (ID number: {}).".format(item.item_name, metrc_id)))
		else:
			frappe.msgprint(_("{} was successfully created in METRC.".format(item.item_name)))
	else:
		update_item(item)
		frappe.msgprint(_("{} was successfully updated in METRC.".format(item.item_name)))


def execute_bloomtrace_integration_request():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	pending_requests = frappe.get_all("Integration Request",
		filters={
			"status": ["IN", ["Queued", "Failed"]],
			"reference_doctype": "Item",
			"integration_request_service": "BloomTrace"
		},
		order_by="creation ASC",
		limit=50)

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
			integration_request.save(ignore_permissions=True)
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
	site_url = urlparse(get_url()).netloc
	bloomtrace_compliance_item_dict = {
		"doctype": "Compliance Item",
		"bloomstack_site": site_url,
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
