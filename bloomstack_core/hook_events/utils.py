import frappe
from erpnext.stock.doctype.item.item import get_uom_conv_factor
from frappe import _
from frappe.utils import getdate, nowdate

DRY_FLOWER_MULTIPLIER = 9.65
DRY_LEAF_MULTIPLER = 2.87
FRESH_PLANT_MULTIPLER = 1.35
EXCISE_TAX_PERCENTAGE = 27


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
	cultivation_tax_account = frappe.db.get_value("Company", doc.company, "default_cultivation_tax_account")
	excise_tax_account = frappe.db.get_value("Company", doc.company, "default_excise_tax_account")
	shipping_account = frappe.db.get_value("Company", doc.company, "default_shipping_account")

	#fetch all compliance item which are enable for cultivation and excise tax calculation
	compliance_items = frappe.get_all('Compliance Item',
		filters={'enable_cultivation_tax': 1},
		fields=['item_code', 'cultivation_tax_type'])
	
	if not compliance_items:
		return

	if doc.doctype in ("Purchase Order", "Purchase Invoice", "Purchase Receipt"):
		if not cultivation_tax_account:
			frappe.throw(_("Please set default cultivation tax account in company {0}").format(doc.company))

		# calculate cultivation tax for buying cycle
		cultivation_tax_row = calculate_cultivation_tax(doc, compliance_items, cultivation_tax_account)
		if cultivation_tax_row:
			set_taxes(doc, cultivation_tax_row)

	elif doc.doctype in ("Sales Order", "Sales Invoice", "Delivery Note"):
		if not excise_tax_account and not shipping_account:
			frappe.throw(_("Please set default excise tax and default shipping account in company {0}").format(doc.company))

		customer_license = frappe.db.get_value("Customer", doc.customer, 'license')
		if not customer_license:
			frappe.throw(_("Please set customer compliance license in customer {0}").format(doc.customer))

		license_type = frappe.db.get_value("Compliance Info", customer_license, "license_type")
		if license_type == "Distributor":
			if not cultivation_tax_account:
				frappe.throw(_("Please set default cultivation tax account in company {0}").format(doc.company))

			# calculate cultivation tax for selling cycle if customer is distributor
			cultivation_tax_row = calculate_cultivation_tax(doc, compliance_items, cultivation_tax_account)
			if cultivation_tax_row:
				set_taxes(doc, cultivation_tax_row)
		else:
			# calculate excise tax for selling cycle except when customer is distributor
			exicse_tax_row = calculate_excise_tax(doc, compliance_items, excise_tax_account, shipping_account)
			if exicse_tax_row:
				set_taxes(doc, exicse_tax_row)


def calculate_cultivation_tax(doc, compliance_items, cultivation_tax_account):
	cultivation_tax = 0

	for item in doc.get("items"):
		compliance_item = next(data for data in compliance_items if data["item_code"] == item.item_code)
		if not compliance_item:
			continue

		tax_type = compliance_item.cultivation_tax_type
		ounce_qty = convert_to_ounce(item.item_name, item.uom, item.stock_qty)

		if tax_type == "Dry Flower":
			cultivation_tax += (ounce_qty * DRY_FLOWER_MULTIPLIER)
		elif tax_type == "Dry Leaf":
			cultivation_tax += (ounce_qty * DRY_LEAF_MULTIPLER)
		elif tax_type == "Fresh Plant":
			cultivation_tax += (ounce_qty * FRESH_PLANT_MULTIPLER)

	cultivation_tax_row = {
		'category': 'Total',
		'charge_type': 'Actual',
		'add_deduct_tax': 'Deduct',
		'description': 'Cultivation Tax',
		'account_head': cultivation_tax_account,
		'tax_amount': cultivation_tax
	}

	return cultivation_tax_row


def calculate_excise_tax(doc, compliance_items, excise_tax_account, shipping_account):
	excise_tax = shipping_charges = 0

	if not excise_tax_account and not shipping_account:
		frappe.throw(_("Please set default excise tax and default shipping account for company {0}").format(doc.company))

	for tax in doc.get("taxes"):
		if tax.account_head == shipping_account:
			shipping_charges = tax.tax_amount

	for item in doc.get("items"):
		compliance_item = next(data for data in compliance_items if data["item_code"] == item.item_code)
		if not compliance_item:
			continue

		# calculate shipping factor for each compliance item in range 0 to 1
		shipping_factor = (shipping_charges / doc.total) * item.price_list_rate

		# calculate excise tax base value
		base_excise_tax = (item.amount * EXCISE_TAX_PERCENTAGE / 100)

		# calculate shipping charges for individual compliance item
		total_shipping_charges = (base_excise_tax / item.price_list_rate) * shipping_factor
		excise_tax += base_excise_tax + total_shipping_charges

	exicse_tax_row = {
		'category': 'Total',
		'add_deduct_tax': 'Add',
		'charge_type': 'Actual',
		'description': 'Excise Tax',
		'account_head': excise_tax_account,
		'tax_amount': excise_tax
	}

	return exicse_tax_row


def set_taxes(doc, tax_row):
	existing_tax_row = doc.get("taxes", filters=tax_row['account_head'])
	if existing_tax_row and existing_tax_row[-1].account_head == tax_row['account_head']:
		# take the last record found
		existing_tax_row[-1].tax_amount = tax_row['tax_amount']
	else:
		doc.append('taxes', tax_row)

	# make sure all total and taxes modified accroding to above tax.
	doc.calculate_taxes_and_totals()


def convert_to_ounce(item_name, uom, qty):
	"convert any unit into ounce"

	conversion_factor = get_uom_conv_factor(uom, 'Ounce')

	if not conversion_factor:
		frappe.throw(_("Add Weight UOM Conversion Factor for {0} to Ounce for item {1}").format(uom, item_name))

	value = qty * conversion_factor
	return value
