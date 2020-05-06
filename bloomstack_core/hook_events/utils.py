import frappe
from frappe import _
from frappe.utils import getdate, nowdate
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

def validate_cannabis_tax(doc, method):
	if doc.doctype in ("Purchase Order", "Purchase Invoice", "Purchase Receipt"):
		cultivation_tax_account = frappe.db.get_value("Company", doc.company, "default_cultivation_tax_account")
		if not cultivation_tax_account:
			frappe.throw(_("Please set default cultivation tax account in company {0}").format(doc.company))

		# calculate cultivation tax for buying cycle and if customer is distributor then caclulate for selling cycle
		cultivation_tax_row = calculate_cultivation_tax(doc, cultivation_tax_account)
		if cultivation_tax_row:
			set_taxes(doc, cultivation_tax_row)

	if doc.doctype in ("Sales Order", "Sales Invoice", "Delivery Note"):
		customer_license = frappe.db.get_value("Customer", doc.customer, 'license')
		license_type = frappe.db.get_value("Compliance Info", customer_license, "license_type")

		cultivation_tax_account = frappe.db.get_value("Company", doc.company, "default_cultivation_tax_account")
		if not cultivation_tax_account:
			frappe.throw(_("Please set default cultivation tax account in company {0}").format(doc.company))

		excise_tax_account = frappe.db.get_value("Company", doc.company, "default_excise_tax_account")
		shipping_account = frappe.db.get_value("Company", doc.company, "default_shipping_account")

		if not excise_tax_account and not shipping_account:
			frappe.throw(_("Please set default excise tax and default shipping account in company {0}").format(doc.company))

		# calculate cultivation tax for buying cycle and if customer is distributor then caclulate for selling cycle
		cultivation_tax_row = calculate_cultivation_tax(doc, cultivation_tax_account, license_type)
		if cultivation_tax_row:
			set_taxes(doc, cultivation_tax_row)

		# calculate excise tax for selling cycle except when customer is distributor
		exicse_tax_row = calculate_excise_tax(doc, excise_tax_account, shipping_account, license_type)
		if exicse_tax_row:
			set_taxes(doc, exicse_tax_row)

def calculate_cultivation_tax(doc, cultivation_tax_account,  license_type = None):
	# if customer is distributor then calculate cultivation tax.
	if not license_type == "Distributor" and doc.doctype in ("Sales Order", "Sales Invoice", "Delivery Note"):
		return 

	cultivation_tax = 0

	for item in doc.get("items"):

		compliance_item = frappe.get_all('Compliance Item',
			filters={'item_code': item.item_code, 'enable_cultivation_tax': 1 },
			fields=['enable_cultivation_tax','cultivation_tax_type'])

		if not compliance_item:
			return

		ounce_qty = convert_to_ounce(item.name, item.weight_uom, item.total_weight)
		if compliance_item[0].cultivation_tax_type == "Dry Flower":
			cultivation_tax = cultivation_tax + ounce_qty * 9.65
		if compliance_item[0].cultivation_tax_type == "Dry Leaf":
			cultivation_tax =  cultivation_tax + ounce_qty * 2.87
		if compliance_item[0].cultivation_tax_type == "Fresh Plant":
			cultivation_tax = cultivation_tax + ounce_qty * 1.35

	cultivation_tax_row = {
		'category':'Total',
		'charge_type':'Actual',
		'add_deduct_tax': 'Deduct',
		'description': 'Cultivation Tax',
		'account_head': cultivation_tax_account,
		'tax_amount': cultivation_tax,
		'total': doc.total - cultivation_tax
		}
	return cultivation_tax_row

def calculate_excise_tax(doc, excise_tax_account, shipping_account, license_type):
	if doc.doctype in ("Sales Order", "Sales Invoice", "Delivery_note"):

		# if customer is distributor then dont calculate excise tax.
		if license_type == "Distributor":
			return

		excise_tax = 0
		shipping_charges = 0

		if not excise_tax_account and not shipping_account:
			frappe.throw(_("Please set default excise tax and default shipping account in company {0}").format(doc.company))

		for tax in doc.get("taxes"):
			if tax.account_head == shipping_account:
				shipping_charges = tax.tax_amount

		for item in doc.get("items"):

			compliance_item = frappe.get_all('Compliance Item',
				filters={'item_code': item.item_code, 'enable_cultivation_tax': 1 },
				fields=['enable_cultivation_tax','cultivation_tax_type'])

			if not compliance_item:
				return

			#calculate shipping facotor for each compliance item in range 0 to 1.
			shipping_factor = ((shipping_charges/doc.total) * item.price_list_rate)

			#calculate shipping charges for individual compliance item
			total_shipping_charges = ((((item.amount  * 27) / 100)/item.price_list_rate) * shipping_factor)
			excise_tax = excise_tax + ((item.amount  * 27) / 100) + total_shipping_charges

		exicse_tax_row = {
			'charge_type':'Actual',
			'description': 'Excise Tax',
			'account_head': excise_tax_account,
			'tax_amount': excise_tax
			}
		return exicse_tax_row

def set_taxes(doc, tax_row):
	existing_tax_row = doc.get("taxes", filters=tax_row['account_head'])
	if existing_tax_row:
		# take the last record found
		existing_tax_row[-1].tax_amount = tax_row['tax_amount']
	else:
		doc.append('taxes', tax_row)

	# make sure all total and taxes modified accroding to above tax.
	doc.calculate_taxes_and_totals()

def convert_to_ounce(item_code, uom, qty):
	"convert any unit into ounce"
	conversion_factor = get_uom_conv_factor(uom, 'Ounce')
	if not conversion_factor:
		frappe.throw(_("Add UOM Conversion Factor for {0} to Ounce").format(uom))
	value = qty * conversion_factor
	return value
