import frappe
from frappe import _
from frappe.utils import getdate, nowdate


def validate_license_expiry(doc, method):
	if doc.doctype in ("Quotation", "Sales Order", "Sales Invoice", "Delivery Note"):
		validate_entity_license(doc.customer)
	elif doc.doctype in ("Purchase Order", "Purchase Invoice", "Purchase Receipt"):
		validate_entity_license(doc.supplier)


@frappe.whitelist()
def validate_entity_license(entity):
	if frappe.db.exists("Compliance Info", {"entity": entity}):
		license_expiry_date, license_number = frappe.db.get_value(
			"Compliance Info", {"entity": entity}, ["license_expiry_date", "license_number"])

		if license_expiry_date and license_expiry_date < getdate(nowdate()):
			frappe.throw(_("{0}'s license number {1} has expired on {2}").format(frappe.bold(
				entity), frappe.bold(license_number), frappe.bold(license_expiry_date)))
