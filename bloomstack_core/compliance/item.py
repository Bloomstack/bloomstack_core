import frappe
from bloomstack_core.utils import get_metrc, log_request
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
		"Id": compliance_item.item.metrc_id,
		"Name": compliance_item.item_name,
		"ItemCategory": compliance_item.item.metrc_item_category,
		"UnitOfMeasure": compliance_item.item.metrc_uom
	}

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
