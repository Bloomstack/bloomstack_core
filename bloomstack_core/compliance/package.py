import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client, make_integration_request
from bloomstack_core.compliance.utils import log_request
from frappe import _
from frappe.utils import cstr


# From Stock Entry
def create_package_from_stock(stock_entry, method):
	# TODO: Handle non-manufacture Stock Entries for intermediate packages
	stock_entry_purpose = frappe.db.get_value("Stock Entry Type", stock_entry.stock_entry_type, "purpose")
	if stock_entry_purpose not in ["Manufacture", "Repack"]:
		return

	make_integration_request("Stock Entry", stock_entry.name)


def adjust_package_from_stock(stock_entry, method):
	# TODO: Handle non-manufacture Stock Entries for intermediate packages
	if stock_entry.stock_entry_type != "Manufacture":
		return


def build_stock_payload(stock_entry):
	"""
	Create the request body for package doctype in bloomtrace from a Stock Entry.

	Args:
		stock_entry (object): The `Stock Entry` Frappe object.

	Returns:
		payload (list of dict): The `Stock Entry` payload, if an Item is moved / created, otherwise `None`.
	"""

	payload = {}
	package_ingredients = []

	for item in stock_entry.items:
		if not frappe.db.get_value("Item", item.item_code, "is_compliance_item"):
			continue

		if item.s_warehouse:
			package_ingredients.append({
				"package": item.package_tag,
				"quantity": item.qty,
				"unit_of_measure": item.uom,
			})
		elif item.t_warehouse:
			payload = {
				"tag": item.package_tag,
				"item": item.item_name,
				"quantity": item.qty,
				"unit_of_measure": item.uom,
				"patient_license_number": "",
				"actual_date": stock_entry.posting_date,
			}

	if not payload:
		return

	payload["doctype"] = "Package"
	payload["ingredients"] = package_ingredients

	return [payload]


def execute_bloomtrace_integration_request_for_stock_entry():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	pending_requests = frappe.get_all("Integration Request", filters={
		"status": ["IN", ["Queued", "Failed"]],
		"reference_doctype": "Stock Entry",
		"integration_request_service": "BloomTrace"
	}, order_by="creation ASC", limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		stock_entry = frappe.get_doc("Stock Entry", integration_request.reference_docname)

		try:
			package = build_stock_payload(stock_entry)
			frappe_client.insert(package)

			integration_request.error = ""
			integration_request.status = "Completed"
		except Exception as e:
			integration_request.error = cstr(e)
			integration_request.status = "Failed"

		integration_request.save(ignore_permissions=True)


def create_package_from_delivery(delivery_note, method):
	if delivery_note.is_return:
		return

	make_integration_request("Delivery Note", delivery_note.name)


def build_delivery_payload(delivery_note, item):
	"""
	Create the request body for package doctype in bloomtrace from a Delivery Note.

	Args:
		delivery_note (object): The `Delivery Note` Frappe object.
		item (object): The `Delivery Note Item` Frappe object.

	Returns:
		payload (list of dict): The `Delivery Note` payload, if an Item is moved / created, otherwise `None`.
	"""

	payload = {}
	package_ingredients = []

	if item.package_tag:
		source_package_tag = frappe.db.get_value("Package Tag", item.package_tag, "source_package_tag")
		if source_package_tag:
			package_ingredients.append({
				"package": source_package_tag,
				"quantity": item.qty,
				"unit_of_measure": item.uom,
			})
		elif item.warehouse:
			payload = {
				"tag": item.package_tag,
				"item": item.item_name,
				"quantity": item.qty,
				"unit_of_measure": item.uom,
				"patient_license_number": "",
				"actual_date": delivery_note.lr_date or delivery_note.posting_date
			}

	if not payload:
		return

	payload["doctype"] = "Package"
	payload["Ingredients"] = package_ingredients

	return [payload]

def execute_bloomtrace_integration_request_for_delivery_note():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	pending_requests = frappe.get_all("Integration Request", filters={
		"status": ["IN", ["Queued", "Failed"]],
		"reference_doctype": "Delivery Note",
		"integration_request_service": "BloomTrace"
	}, order_by="creation ASC", limit=50)

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		delivery_note = frappe.get_doc("Delivery Note", integration_request.reference_docname)

		for item in delivery_note.items:
			if not frappe.db.get_value("Item", item.item_code, "is_compliance_item") or not item.package_tag:
				continue

			try:
				package = build_delivery_payload(delivery_note, item)
				frappe_client.insert(package)

				integration_request.error = ""
				integration_request.status = "Completed"
			except Exception as e:
				integration_request.error = cstr(e)
				integration_request.status = "Failed"

			integration_request.save(ignore_permissions=True)
