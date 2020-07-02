import frappe
from erpnext.stock.doctype.delivery_note.delivery_note import update_delivery_note_status as update_dn_status


def update_delivery_note_status(payment_entry, method):
	sales_invoices = [ref.reference_name for ref in payment_entry.references
		if ref.reference_doctype == "Sales Invoice"]

	if not sales_invoices:
		return

	delivery_notes = frappe.get_all("Delivery Note",
		filters=[
			["Delivery Note Item", "against_sales_invoice", "IN", sales_invoices]
		],
		fields=["name", "status"],
		distinct=True)

	if not delivery_notes:
		return

	for delivery_note in delivery_notes:
		if method == "on_submit" and delivery_note.status == "Completed":
			update_dn_status(delivery_note.name, "Closed")
		elif method == "on_cancel" and delivery_note.status == "Closed":
			update_dn_status(delivery_note.name, "Completed")
