import frappe
from bloomstack_core.hook_events.utils import get_default_license
from erpnext.stock.doctype.item.item import get_uom_conv_factor
from frappe import _

DRY_FLOWER_TAX_RATE = 9.65
DRY_LEAF_TAX_RATE = 2.87
FRESH_PLANT_TAX_RATE = 1.35
EXCISE_TAX_RATE = 15
MARKUP_PERCENTAGE = 80


def calculate_cannabis_tax(doc, method):
	compliance_items = frappe.get_all('Compliance Item', fields=['item_code', 'enable_cultivation_tax', 'item_category'])

	if not compliance_items:
		return

	if doc.doctype in ("Purchase Order", "Purchase Invoice", "Purchase Receipt"):
		# calculate cultivation tax for buying cycle
		cultivation_tax_row = calculate_cultivation_tax(doc, compliance_items)
		set_taxes(doc, cultivation_tax_row)
	elif doc.doctype in ("Quotation", "Sales Order", "Sales Invoice", "Delivery Note"):
		# customer license is required to inspect license type
		if doc.doctype == "Quotation" and doc.quotation_to == "Customer":
			default_customer_license = get_default_license("Customer", doc.party_name)
		elif doc.doctype in ("Sales Order", "Sales Invoice", "Delivery Note"):
			default_customer_license = get_default_license("Customer", doc.customer)
		else:
			return

		if not default_customer_license:
			frappe.msgprint(_("Please set a default license for {0} to calculate taxes").format(doc.customer))
			return

		license_for = frappe.db.get_value("Compliance Info", default_customer_license, "license_for")
		if license_for == "Distributor":
			# calculate cultivation tax for selling cycle if customer is a distributor
			cultivation_tax_row = calculate_cultivation_tax(doc, compliance_items)
			set_taxes(doc, cultivation_tax_row)
		elif license_for == "Retailer":
			# calculate excise tax for selling cycle is customer is a retailer or end-consumer
			exicse_tax_row = calculate_excise_tax(doc, compliance_items)
			set_taxes(doc, exicse_tax_row)


def calculate_cultivation_tax(doc, compliance_items):
	cultivation_tax = 0

	for item in doc.items:
		compliance_item = next((data for data in compliance_items if data.get("item_code") == item.item_code), None)
		if not compliance_item or not compliance_item.enable_cultivation_tax:
			continue

		qty_in_ounces = convert_to_ounces(item.uom, item.qty)

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

	for tax in doc.taxes:
		if tax.account_head == doc.get_company_default("default_shipping_account"):
			total_shipping_charge += tax.tax_amount

	for item in doc.items:
		compliance_item = next((data for data in compliance_items if data.get("item_code") == item.item_code), None)
		if not compliance_item:
			continue

		# calculate the total excist tax for each item
		item_shipping_charge = (total_shipping_charge / doc.total) * (item.price_list_rate * item.qty)
		item_cost_with_shipping = (item.price_list_rate * item.qty) + item_shipping_charge
		item_cost_after_markup = item_cost_with_shipping + (item_cost_with_shipping * MARKUP_PERCENTAGE / 100)
		total_excise_tax += item_cost_after_markup * EXCISE_TAX_RATE / 100

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
	if not tax_row.get("tax_amount"):
		return

	existing_tax_row = doc.get("taxes", filters={"account_head": tax_row.get('account_head')})

	# update an existing tax row, or create a new one
	if existing_tax_row:
		existing_tax_row[-1].tax_amount = tax_row.get('tax_amount', 0)
	else:
		doc.append('taxes', tax_row)

	# make sure all total and taxes are modified based on the new tax
	doc.calculate_taxes_and_totals()


def convert_to_ounces(uom, qty):
	conversion_factor = get_uom_conv_factor(uom, 'Ounce')

	if not conversion_factor:
		frappe.throw(_("Please set Conversion Factor for {0} to Ounce").format(uom))

	qty_in_ounce = qty * conversion_factor

	return qty_in_ounce
