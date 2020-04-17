import frappe
from frappe import _
from frappe.utils import getdate, nowdate

def validate_license_expiry(doc, method=None):
    if doc.doctype in ("Sales Order", "Sales Invoice", "Delivery Note"):
        validate_entity(doc.customer)
       
    if doc.doctype in ("Purchase Order", "Purchase Invoice", "Purchase Receipt"):
        validate_entity(doc.supplier)

def validate_entity(entity):
    compliance_info = frappe.db.get_value("Compliance Info", {"entity":entity}, ["license_expiry_date","license_number"], as_dict=True)
    if compliance_info.license_expiry_date and compliance_info.license_expiry_date < getdate(nowdate()):
        frappe.throw(_("You are not allowed to do Transaction. Entity {0} license number {1} expired on {2}").format(frappe.bold(entity), frappe.bold(compliance_info.license_number), frappe.bold(compliance_info.license_expiry_date)))