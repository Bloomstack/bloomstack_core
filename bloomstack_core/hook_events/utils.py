import frappe
from frappe import _
from frappe.utils import getdate, nowdate


def validate_license_expiry(doc, method):
	if doc.doctype in ("Quotation", "Sales Order", "Sales Invoice", "Delivery Note"):
		validate_entity_license("Customer", doc.customer)
	elif doc.doctype in ("Purchase Order", "Purchase Invoice", "Purchase Receipt"):
		validate_entity_license("Supplier", doc.supplier)


@frappe.whitelist()
def validate_entity_license(party_type, party_name):
	license_record = frappe.db.get_value(party_type, party_name, "license")

	if not license_record:
		return

	license_expiry_date, license_number = frappe.db.get_value(
		"Compliance Info", license_record, ["license_expiry_date", "license_number"])

	if license_expiry_date and license_expiry_date < getdate(nowdate()):
		frappe.throw(_("{0}'s license number {1} has expired on {2}").format(
			frappe.bold(party_name), frappe.bold(license_number), frappe.bold(license_expiry_date)))

def validate_cultivation_tax(doc, method):
	if doc.doctype in ("Purchase Order", "Purchase Invoice", "Purchase Receipt"):
		items = []
		for d in doc.get("items"):

			cultivated_item = frappe.db.sql("""select enable_cultivation_tax,
				cultivation_tax_type from `tabComplaince Item` where item_code=%s""",
				d.item_code, as_dict=1)[0]

			if not cultivated_item.enable_cultivation_tax:
				return
			# else:
			# 	# calculate_cultivation_tax()

			items.append(cstr(d.item_code))

# def check_cultivation_tax(item_code, docname):
	# pass
	