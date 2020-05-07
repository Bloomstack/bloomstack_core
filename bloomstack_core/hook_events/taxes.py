import frappe
from frappe import _
from erpnext.stock.doctype.item.item import get_uom_conv_factor

DRY_FLOWER_TAX_RATE = 9.65
DRY_LEAF_TAX_RATE = 2.87
FRESH_PLANT_TAX_RATE = 1.35
EXCISE_TAX_RATE = 15
MARKUP_PERCENTAGE = 80

def calculate_cannabis_tax(doc, method):
	compliance_items = frappe.get_all('Compliance Item',
		fields=['item_code', 'enable_cultivation_tax', 'item_category'])
	
	if not compliance_items:
		return

	if doc.doctype in ("Purchase Order", "Purchase Invoice", "Purchase Receipt"):
		# calculate cultivation tax for buying cycle
		cultivation_tax_row = calculate_cultivation_tax(doc, compliance_items)
		
		if cultivation_tax_row:
			set_taxes(doc, cultivation_tax_row)

	elif doc.doctype in ("Quotation", "Sales Order", "Sales Invoice", "Delivery Note"):
		customer_license = frappe.db.get_value("Customer", doc.customer, 'license')
		#customer license is important for fetching customer license type
		if not customer_license:
			return

		license_type = frappe.db.get_value("Compliance Info", customer_license, "license_type")
		if license_type == "Distributor":
			# calculate cultivation tax for selling cycle if customer is distributor
			cultivation_tax_row = calculate_cultivation_tax(doc, compliance_items)

			if cultivation_tax_row:
				set_taxes(doc, cultivation_tax_row)

		elif license_type in ("Retailer", "Consumer"):
			# calculate excise tax for selling cycle 
			exicse_tax_row = calculate_excise_tax(doc, compliance_items)
			
			if exicse_tax_row:
				set_taxes(doc, exicse_tax_row)
			
		else:
			return


def calculate_cultivation_tax(doc, compliance_items):
	cultivation_tax = 0

	for item in doc.get("items"):
		compliance_item = next((data for data in compliance_items if data["item_code"] == item.item_code), None)
		if not compliance_item and not compliance_item.enable_cultivation_tax:
			continue

		qty_in_ounces = convert_to_ounce(item.uom, item.qty)

		if compliance_item.item_category == "Dry Flower":
			cultivation_tax += (qty_in_ounces * DRY_FLOWER_TAX_RATE)
		elif compliance_item.item_category == "Dry Leaf":
			cultivation_tax += (qty_in_ounces * DRY_LEAF_TAX_RATE)
		elif compliance_item.item_category == "Fresh Plant":
			cultivation_tax += (qty_in_ounces * FRESH_PLANT_TAX_RATE)

	cultivation_tax_row = {
		'category': 'Total',
		'charge_type': 'Actual',
		'add_deduct_tax': 'Deduct',
		'description': 'Cultivation Tax',
		'account_head': doc.get_company_default("default_cultivation_tax_account"),
		'tax_amount': cultivation_tax
	}

	return cultivation_tax_row


def calculate_excise_tax(doc, compliance_items):
	total_excise_tax = total_shipping_charge = 0

	for tax in doc.get("taxes"):
		if tax.account_head == doc.get_company_default("default_shipping_account"):
			total_shipping_charge = tax.tax_amount

	for item in doc.get("items"):
		compliance_item = next((data for data in compliance_items if data["item_code"] == item.item_code), None)

		if not compliance_item:
			continue

		# calculate shipping charge for item
		item_shipping_charge = (total_shipping_charge / doc.total) * (item.price_list_rate * item.qty)

		total_item_cost = (item.price_list_rate * item.qty) + item_shipping_charge
		
		total_excise_tax += ((total_item_cost * MARKUP_PERCENTAGE / 100 ) * EXCISE_TAX_RATE /100 )

	exicse_tax_row = {
		'category': 'Total',
		'add_deduct_tax': 'Add',
		'charge_type': 'Actual',
		'description': 'Excise Tax',
		'account_head': doc.get_company_default("default_excise_tax_account"),
		'tax_amount': total_excise_tax
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


def convert_to_ounce(uom, qty):
	conversion_factor = get_uom_conv_factor(uom, 'Ounce')

	if not conversion_factor:
		frappe.throw(_("Please set Conversion Factor for {0} to Ounce").format(uom))

	qty_in_ounce = qty * conversion_factor
	
	return qty_in_ounce
