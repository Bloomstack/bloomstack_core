import frappe
from bloomstack_core.compliance.utils import get_metrc, log_request
from frappe import _


def create_package_from_stock(stock_entry, method):
	# TODO: Handle non-manufacture Stock Entries for intermediate packages
	stock_entry_purpose = frappe.db.get_value("Stock Entry Type", stock_entry.stock_entry_type, "purpose")
	if stock_entry_purpose not in ["Manufacture", "Repack"]:
		return

	metrc = get_metrc()

	if not metrc:
		return

	payload = build_stock_payload(stock_entry)
	response = metrc.packages.create.post(json=payload)
	log_request(response.url, payload, response, "Stock Entry", stock_entry.name)

	if not response.ok:
		frappe.throw(_(response.raise_for_status()))


def adjust_package_from_stock(stock_entry, method):
	# TODO: Handle non-manufacture Stock Entries for intermediate packages
	if stock_entry.stock_entry_type != "Manufacture":
		return


def build_stock_payload(stock_entry):
	"""
	Create the request body for package generation from a Stock Entry.

	Args:
		stock_entry (object): The `Stock Entry` Frappe object.

	Returns:
		payload (list of dict): The `Stock Entry` payload, if a Compliance Item is moved / created, otherwise `None`.
	"""

	payload = {}
	package_ingredients = []

	for item in stock_entry.items:
		if not frappe.db.exists("Compliance Item", item.item_code):
			continue

		if item.s_warehouse:
			package_ingredients.append({
				"Package": item.package_tag,
				"Quantity": item.qty,
				"UnitOfMeasure": item.uom,
			})
		elif item.t_warehouse:
			payload = {
				"Tag": item.package_tag,
				"Item": item.item_name,
				"Quantity": item.qty,
				"UnitOfMeasure": item.uom,
				"PatientLicenseNumber": "",
				"ActualDate": stock_entry.posting_date,
			}

	if not payload:
		return

	payload["Ingredients"] = package_ingredients
	payload = [payload]
	return payload


def create_package_from_delivery(delivery_note, method):
	if delivery_note.is_return:
		return

	metrc = get_metrc()

	if not metrc:
		return

	for item in delivery_note.items:
		if not frappe.db.exists("Compliance Item", item.item_code):
			continue

		if not item.package_tag:
			continue

		payload = build_delivery_payload(delivery_note, item)
		response = metrc.packages.create.post(json=payload)
		log_request(response.url, payload, response, "Delivery Note Item", item.name)

		if not response.ok:
			frappe.throw(_(response.raise_for_status()))


def build_delivery_payload(delivery_note, item):
	"""
	Create the request body for package generation from a Delivery Note.

	Args:
		delivery_note (object): The `Delivery Note` Frappe object.
		item (object): The `Delivery Note Item` Frappe object.

	Returns:
		payload (list of dict): The `Delivery Note` payload, if a Compliance Item is moved / created, otherwise `None`.
	"""

	payload = {}
	package_ingredients = []

	if item.package_tag:
		source_package_tag = frappe.db.get_value("Package Tag", item.package_tag, "source_package_tag")
		if source_package_tag:
			package_ingredients.append({
				"Package": source_package_tag,
				"Quantity": item.qty,
				"UnitOfMeasure": item.uom,
			})
		elif item.warehouse:
			payload = {
				"Tag": item.package_tag,
				"Item": item.item_name,
				"Quantity": item.qty,
				"UnitOfMeasure": item.uom,
				"PatientLicenseNumber": "",
				"ActualDate": delivery_note.lr_date or delivery_note.posting_date
			}

	if not payload:
		return

	payload["Ingredients"] = package_ingredients
	payload = [payload]
	return payload
