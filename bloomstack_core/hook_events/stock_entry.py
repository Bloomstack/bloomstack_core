import frappe
from bloomstack_core.bloomtrace import make_integration_request, get_bloomtrace_client
from frappe.utils import cstr

def add_comment_to_batch(stock_entry, method):
	for item in stock_entry.items:
		if item.batch_no:
			if item.s_warehouse:
				comment_text = "{qty} {uom} consumed by {stock_entry}".format(
					qty=item.qty, uom=item.uom, stock_entry=stock_entry.name)
			elif item.t_warehouse:
				comment_text = "{qty} {uom} created from {stock_entry}".format(
					qty=item.qty, uom=item.uom, stock_entry=stock_entry.name)

			batch_doc = frappe.get_doc("Batch", item.batch_no)
			comment = batch_doc.add_comment(comment_type="Comment", text=comment_text)
			comment.comment_type = "Info"
			comment.save()

	frappe.db.commit()

def create_package_from_stock(stock_entry, method):
	# TODO: Handle non-manufacture Stock Entries for intermediate packages
	stock_entry_purpose = frappe.db.get_value("Stock Entry Type", stock_entry.stock_entry_type, "purpose")
	if stock_entry_purpose not in ["Manufacture", "Repack"]:
		return

	make_integration_request("Stock Entry", stock_entry.name, "Package")

def execute_bloomtrace_integration_request():
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
			integration_request.error = cstr(frappe.get_traceback())
			integration_request.status = "Failed"

		integration_request.save(ignore_permissions=True)

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
	payload["bloomstack_company"] = stock_entry.company

	return payload
