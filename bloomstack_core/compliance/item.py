import frappe
from bloomstack_core.compliance.utils import get_metrc, log_request
from frappe import _


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

	compliance_item = frappe.get_doc("Compliance Item", item.item_code)

	item_data = {
		"Name": compliance_item.item_name,
		"ItemCategory": compliance_item.metrc_item_category,
		"UnitOfMeasure": compliance_item.metrc_uom
	}

	if compliance_item.metrc_id:
		item_data.update({
			"Id": compliance_item.metrc_id
		})

	mandatory_metrc_unit = frappe.db.get_value("Compliance Item Category", compliance_item.metrc_item_category, "mandatory_unit")

	if mandatory_metrc_unit == "Volume":
		item_data.update({
			"UnitVolume": compliance_item.metrc_unit_value,
			"UnitVolumeUnitOfMeasure": compliance_item.metrc_unit_uom
		})
	elif mandatory_metrc_unit == "Weight":
		item_data.update({
			"UnitWeight": compliance_item.metrc_unit_value,
			"UnitWeightUnitOfMeasure": compliance_item.metrc_unit_uom
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
