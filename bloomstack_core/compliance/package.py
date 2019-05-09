import frappe
from bloomstack_core.utils import get_metrc, log_request
from frappe import _


def create_package(stock_entry, method):
	# TODO: Handle non-manufacture Stock Entries for intermediate packages
	if stock_entry.purpose != "Manufacture":
		return

	metrc = get_metrc()

	if not metrc:
		return

	payload = build_payload(stock_entry)
	response = metrc.packages.create.post(json=payload)
	log_request(response.url, payload, response, "Stock Entry", stock_entry.name)

	if not response.ok:
		frappe.throw(_(response.raise_for_status()))


def adjust_package(stock_entry, method):
	# TODO: Handle non-manufacture Stock Entries for intermediate packages
	if stock_entry.purpose != "Manufacture":
		return


def build_payload(stock_entry):
	"""
	Create the request body for the Item endpoint.

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
