import json

import frappe
from bloomstack_core.hook_events.delivery_trip import make_payment_entry
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_return


@frappe.whitelist()
def collect(amount, delivery_note, sales_invoice=None, returned_items=None):
	"""
	Make a Payment Entry for the received amount against a delivery.

	If all the items are not delivered, then create a return Delivery Note against the returned items.

	Args:
		amount (float): The amount paid for the delivery.
		delivery_note (str): The reference Delivery Note that contains order info.
		sales_invoice (str, optional): The reference Sales Invoice against which the payment is made.
		returned_items (str, optional): Any delivered items that have been returned. Defaults to None.
			Example: '[
				{
					"reason": "Reason for rejection",
					"item_code": "VC-CB-SSB-0001",
					"qty": 1.0
				},
				...
			]'

	Returns:
		dict: The generated draft Payment Entry ID and, if applicable, the return Delivery Note ID
			Example: {
				"payment_id": "ACC-PAY-2020-0001",
				"return_delivery_id": "DN-0001"
			}
	"""

	# generate a payment entry for the delivered items
	if not sales_invoice:
		invoices = frappe.get_all("Delivery Note Item",
			filters={"docstatus": 1, "parent": delivery_note},
			fields=["distinct(against_sales_invoice)"])

		if invoices:
			sales_invoice = invoices[0].against_sales_invoice

	if not sales_invoice:
		return {"error": "No invoice found to make payment against"}

	payment_id = make_payment_entry(amount, sales_invoice)

	# generate a return delivery note, if applicable
	return_delivery_id = None
	if returned_items:
		return_delivery_id = make_return_delivery(delivery_note, returned_items)

	# return payment and return info
	return {
		"payment_id": payment_id,
		"return_delivery_id": return_delivery_id
	}


def make_return_delivery(delivery_note, returned_items):
	"""
	If all the ordered items are not delivered, create a return Delivery Note against the returned items.

	Args:
		delivery_note (str): The reference Delivery Note that contains order info.
		returned_items (str): Any delivered items that have been returned.
			Example: '[
				{
					"reason": "Reason for rejection",
					"item_code": "VC-CB-SSB-0001",
					"qty": 1.0
				},
				...
			]'

	Returns:
		str: The generated draft return Delivery Note ID
	"""

	if isinstance(returned_items, str):
		returned_items = json.loads(returned_items)

	if isinstance(returned_items, list):
		returned_items_map = {d.get("item_code"): d.get("qty") for d in returned_items}
		return_delivery = make_sales_return(delivery_note)

		for item in return_delivery.items:
			returned_item = next((_item for _item in returned_items if _item.get("item_code") == item.item_code), None)

			if not returned_item:
				item.qty = 0
			else:
				item.qty = -returned_item.get("qty") or -item.qty
				item.reason_for_return = returned_item.get("reason")

		return_delivery.save()
		return_delivery_id = return_delivery.name

		return return_delivery_id
