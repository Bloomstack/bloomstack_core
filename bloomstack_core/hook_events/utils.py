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
		cultivated_tax = 0
		for d in doc.get("items"):

			cultivated_item = frappe.db.sql("""select enable_cultivation_tax,
				cultivation_tax_type from `tabComplaince Item` where item_code=%s""",
				d.item_code, as_dict=1)[0]

			if not cultivated_item.enable_cultivation_tax:
				return
			else:
				ounce_qty = convert_ounce(d.stock_qty)
				if cultivated_item.cultivation_tax_type == "Dry Flower"
					cultivated_tax = cultivated_tax +  ounce_qty * 9.65
				if cultivated_item.cultivation_tax_type == "Dry Leaf"
					cultivated_tax =  cultivated_tax + ounce_qty * 2.87
				if cultivated_item.cultivation_tax_type == "Fresh Plant"
					cultivated_tax = cultivated_tax + ounce_qty * 1.35
				# calculate_cultivation_tax()

			items.append(cstr(d.item_code))

# def check_cultivation_tax(item_code, docname):
	# pass
	
def convert_ounce(qty):
	"convert grams to ounce"

	g_to_oz_value = 28.35
	return qty/g_to_oz_value