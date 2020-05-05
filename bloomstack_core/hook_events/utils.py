import frappe
from frappe import _
from frappe.utils import getdate, nowdate
from frappe.utils import cstr
from erpnext.stock.doctype.item.item import get_uom_conv_factor


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
	if doc.doctype in ("Purchase Order", "Purchase Invoice", "Purchase Receipt", "Sales Order", "Sales Invoice", "Delivery_note"):

		# if customer is distributor then calculate cultivation tax.
		customer_license = frappe.db.get_value("Customer", filters= {"name": doc.customer}, fieldname=['license'])
		license_type = frappe.db.get_value("Compliance Info", filters={"name":customer_license}, fieldname=["license_type"])
		if not license_type == "Distributor" and doc.doctype in ("Sales Order", "Sales Invoice", "Delivery_note"):
			return 
		
		cultivation_tax = 0
		cultivation_tax_account = frappe.db.get_value("Company", doc.company, "default_cultivation_tax_account")
		if not cultivation_tax_account:
			frappe.throw(_("Please set default cultivation account in company {0}").format(doc.company))

		for item in doc.get("items"):

			compliance_item = frappe.get_all('Compliance Item',
				filters={'item_code': item.item_code},
				fields=['enable_cultivation_tax','cultivation_tax_type'])

			if not compliance_item:
				return
			else:
				compliance_item = compliance_item[0]

			if not compliance_item.enable_cultivation_tax:
				return
			else:
				ounce_qty = convert_to_ounce(item.name, item.weight_uom, item.total_weight)
				if compliance_item.cultivation_tax_type == "Dry Flower":
					cultivation_tax = cultivation_tax +  ounce_qty * 9.65
				if compliance_item.cultivation_tax_type == "Dry Leaf":
					cultivation_tax =  cultivation_tax + ounce_qty * 2.87
				if compliance_item.cultivation_tax_type == "Fresh Plant":
					cultivation_tax = cultivation_tax + ounce_qty * 1.35
		
		cultivation_tax_row = {
			'category':'Total',
			'charge_type':'Actual',
			'add_deduct_tax': 'Deduct',
			'description': 'Cultivation Tax',
			'account_head': cultivation_tax_account,
			'tax_amount': cultivation_tax,
			'total': doc.total-cultivation_tax
			}
		doc.append('taxes', cultivation_tax_row)


def validate_excise_tax(doc, method):
	if doc.doctype in ("Sales Order", "Sales Invoice", "Delivery_note"):

		# if customer is distributor then dont calculate excise tax.
		customer_license = frappe.db.get_value("Customer", filters= {"name": doc.customer}, fieldname=['license'])
		license_type = frappe.db.get_value("Compliance Info", filters={"name":customer_license}, fieldname=["license_type"])
		if license_type == "Distributor":
			return 

		excise_tax = 0
		shipping_charges = 0
		excise_tax_account = frappe.db.get_value("Company", doc.company, "default_excise_tax_account")
		shipping_account = frappe.db.get_value("Company", doc.company, "default_shipping_account")

		if not excise_tax_account and not shipping_account:
			frappe.throw(_("Please set default excise tax and default shipping account in company {0}").format(doc.company))

		for tax in doc.get("taxes"):
			if tax.account_head == shipping_account:
				shipping_charges = tax.amount

		for item in doc.get("items"):

			compliance_item = compliance_item = frappe.get_all('Compliance Item',
				filters={'item_code': item.item_code},
				fields=['enable_cultivation_tax','cultivation_tax_type'])

			if not compliance_item.enable_cultivation_tax:
				return
			else:
				total_shipping_charges = ((shipping_charges/doc.net_total) * item.price_list_rate)
				excise_tax = excise_tax + ((item.amount * 27) / 100) + total_shipping_charges

		exicse_tax_row = {
			'category':'Total',
			'charge_type':'Actual',
			'add_deduct_tax': 'Add',
			'description': 'Excise Tax',
			'account_head': excise_tax_account,
			'tax_amount': excise_tax,
			'total': doc.total + excise_tax
			}
		doc.append('taxes', exicse_tax_row)
	
def convert_to_ounce(item_code, uom, qty):
	"convert any unit into ounce"
	conversion_factor = get_uom_conv_factor(uom, 'Ounce')
	if not conversion_factor:
		frappe.throw(_("Add UOM Conversion Factor for {0} to Ounce").format(uom))
	value = qty * conversion_factor
	return value
