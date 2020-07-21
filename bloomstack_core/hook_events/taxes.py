import json

import frappe
from bloomstack_core.hook_events.utils import get_default_license
from erpnext.accounts.utils import get_company_default
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
		cultivation_taxes = calculate_cultivation_tax(doc)
		for account, tax in cultivation_taxes.items():
			cultivation_tax_row = get_cultivation_tax_row(account, tax)
			set_taxes(doc, cultivation_tax_row)
	elif doc.doctype in ("Quotation", "Sales Order", "Sales Invoice", "Delivery Note"):
		# customer license is required to inspect license type
		if doc.doctype == "Quotation":
			if doc.quotation_to != "Customer":
				return
			default_customer_license = get_default_license("Customer", doc.party_name)
		elif doc.doctype in ("Sales Order", "Sales Invoice", "Delivery Note"):
			default_customer_license = get_default_license("Customer", doc.customer)

		if not default_customer_license:
			frappe.msgprint(_("Please set a default license for {0} to calculate taxes").format(doc.customer))
			return

		license_for = frappe.db.get_value("Compliance Info", default_customer_license, "license_for")
		if license_for == "Distributor":
			# calculate cultivation tax for selling cycle if customer is a distributor
			cultivation_taxes = calculate_cultivation_tax(doc)
			for account, tax in cultivation_taxes.items():
				cultivation_tax_row = get_cultivation_tax_row(account, tax)
				set_taxes(doc, cultivation_tax_row)
		elif license_for == "Retailer":
			# calculate excise tax for selling cycle is customer is a retailer or end-consumer
			excise_tax_row = calculate_excise_tax(doc, compliance_items)
			set_taxes(doc, excise_tax_row)


def calculate_cultivation_tax(doc):
	cultivation_taxes = {}
	for item in doc.get("items"):
		cultivation_taxes = calculate_item_cultivation_tax(doc, item, cultivation_taxes)

	return cultivation_taxes


def calculate_item_cultivation_tax(doc, item, cultivation_taxes=None):
	compliance_items = frappe.get_all('Compliance Item', fields=['item_code', 'enable_cultivation_tax', 'item_category'])
	compliance_item = next((data for data in compliance_items if data.get("item_code") == item.get("item_code")), None)
	if not compliance_item or not compliance_item.enable_cultivation_tax:
		return

	flower_tax_account = get_company_default(doc.get("company"), "default_cultivation_tax_account_flower")
	leaf_tax_account = get_company_default(doc.get("company"), "default_cultivation_tax_account_leaf")
	plant_tax_account = get_company_default(doc.get("company"), "default_cultivation_tax_account_plant")

	if not cultivation_taxes:
		cultivation_taxes = dict.fromkeys([flower_tax_account, leaf_tax_account, plant_tax_account], float())

	qty_in_ounces = convert_to_ounces(item.get("uom"), item.get("qty"))

	if compliance_item.item_category == "Dry Flower":
		cultivation_tax = qty_in_ounces * DRY_FLOWER_TAX_RATE
		cultivation_taxes[flower_tax_account] += cultivation_tax
	elif compliance_item.item_category == "Dry Leaf":
		cultivation_tax = qty_in_ounces * DRY_LEAF_TAX_RATE
		cultivation_taxes[leaf_tax_account] += cultivation_tax
	elif compliance_item.item_category == "Fresh Plant":
		cultivation_tax = qty_in_ounces * FRESH_PLANT_TAX_RATE
		cultivation_taxes[plant_tax_account] += cultivation_tax
	elif compliance_item.item_category == "Based on Raw Materials":
		# calculate cultivation tax based on weight of raw materials
		if not item.get("cultivation_weight_uom"):
			frappe.throw(_("Row #{0}: Please set a cultivation weight UOM".format(item.get("idx"))))

		if item.get("flower_weight"):
			flower_weight_in_ounce = convert_to_ounces(item.get("cultivation_weight_uom"), item.get("flower_weight"))
			flower_cultivation_tax = (flower_weight_in_ounce * DRY_FLOWER_TAX_RATE)
			cultivation_taxes[flower_tax_account] += flower_cultivation_tax

		if item.get("leaf_weight"):
			leaf_weight_in_ounce = convert_to_ounces(item.get("cultivation_weight_uom"), item.get("leaf_weight"))
			leaf_cultivation_tax = (leaf_weight_in_ounce * DRY_LEAF_TAX_RATE)
			cultivation_taxes[leaf_tax_account] += leaf_cultivation_tax

		if item.get("plant_weight"):
			plant_weight_in_ounce = convert_to_ounces(item.get("cultivation_weight_uom"), item.get("plant_weight"))
			plant_cultivation_tax = (plant_weight_in_ounce * FRESH_PLANT_TAX_RATE)
			cultivation_taxes[plant_tax_account] += plant_cultivation_tax

	return cultivation_taxes


def get_cultivation_tax_row(cultivation_tax_account, cultivation_tax_amount):
	cultivation_tax_row = {
		'category': 'Total',
		'charge_type': 'Actual',
		'add_deduct_tax': 'Deduct',
		'description': 'Cultivation Tax',
		'account_head': cultivation_tax_account,
		'tax_amount': cultivation_tax_amount
	}
	return cultivation_tax_row


def calculate_excise_tax(doc, compliance_items):
	total_excise_tax = total_shipping_charge = 0

	if doc.get("taxes"):
		for tax in doc.get("taxes"):
			if tax.get("account_head") == get_company_default(doc.get("company"), "default_shipping_account"):
				total_shipping_charge += tax.tax_amount

	for item in (doc.get("items") or []):
		compliance_item = next((data for data in compliance_items if data.get("item_code") == item.get("item_code")), None)
		if not compliance_item:
			continue

		# fetch either the transaction rate or price list rate, whichever is higher
		price_list_rate = item.get("price_list_rate") or 0
		rate = item.get("rate") or 0
		max_item_rate = max([price_list_rate, rate])
		if max_item_rate == 0:
			continue

		if not doc.net_total:
			return

		# calculate the total excise tax for each item
		item_shipping_charge = (total_shipping_charge / doc.net_total) * (max_item_rate * item.get("qty"))
		item_cost_with_shipping = (max_item_rate * item.get("qty")) + item_shipping_charge
		item_cost_after_markup = item_cost_with_shipping + (item_cost_with_shipping * MARKUP_PERCENTAGE / 100)
		total_excise_tax += item_cost_after_markup * EXCISE_TAX_RATE / 100

	excise_tax_row = {
		'category': 'Total',
		'add_deduct_tax': 'Add',
		'charge_type': 'Actual',
		'description': 'Excise Tax',
		'account_head': get_company_default(doc.get("company"), "default_excise_tax_account"),
		'tax_amount': total_excise_tax
	}

	return excise_tax_row


def set_taxes(doc, tax_row):
	if not tax_row:
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


@frappe.whitelist()
def set_excise_tax(doc):
	if isinstance(doc, str):
		doc = frappe._dict(json.loads(doc))

	compliance_items = frappe.get_all('Compliance Item', fields=['item_code'])
	if not compliance_items:
		return

	excise_tax_row = calculate_excise_tax(doc, compliance_items)
	return excise_tax_row


@frappe.whitelist()
def get_cultivation_tax(doc, items):
	if isinstance(doc, str):
		doc = frappe._dict(json.loads(doc))

	items = json.loads(items)

	for item in items:
		tax = sum(calculate_item_cultivation_tax(doc, item).values())
		item['amount'] = float(item.get("amount")) + tax

	return items
