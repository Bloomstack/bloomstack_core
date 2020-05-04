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
		customer_group = frappe.db.get_value("Customer", filters= {"name": doc.customer}, fieldname=['customer_group'])
		if not customer_group == "Distributor" and doc.doctype in ("Sales Order", "Sales Invoice", "Delivery_note"):
			return 
		
		cultivated_tax = 0
		cultivated_tax_account = ""
		cannabis_account_heads = get_account_heads(doc.company)
		for account_head in cannabis_account_heads:
			cultivated_tax_account = account_head.get("cultivation_tax_account")

		for d in doc.get("items"):

			cultivated_item = frappe.db.sql("""select enable_cultivation_tax,
				cultivation_tax_type from `tabCompliance Item` where item_code=%s""",
				d.item_code, as_dict=1)[0]

			if not cultivated_item.enable_cultivation_tax:
				return
			else:
				ounce_qty = convert_to_ounce(d.name, d.weight_uom, d.total_weight)
				if cultivated_item.cultivation_tax_type == "Dry Flower":
					cultivated_tax = cultivated_tax +  ounce_qty * 9.65
				if cultivated_item.cultivation_tax_type == "Dry Leaf":
					cultivated_tax =  cultivated_tax + ounce_qty * 2.87
				if cultivated_item.cultivation_tax_type == "Fresh Plant":
					cultivated_tax = cultivated_tax + ounce_qty * 1.35
		
		cannabis_account_heads = get_account_heads(doc.company)
		row = doc.append('taxes', {})
		row.category = 'Total'
		row.charge_type = "Actual"
		row.add_deduct_tax = "Deduct"
		row.description = "Cultivation Tax"
		row.account_head = cultivated_tax_account
		row.tax_amount = cultivated_tax
		row.total = doc.total - cultivated_tax

def validate_excise_tax(doc, method):
	if doc.doctype in ("Sales Order", "Sales Invoice", "Delivery_note"):

		# if customer is distributor then dont calculate excise tax.
		customer_group = frappe.db.get_value("Customer", filters= {"name": doc.customer}, fieldname=['customer_group'])
		if customer_group == "Distributor":
			return 

		excise_tax = 0
		shipping_charges = 0
		excise_tax_account = ""
		shipping_account = ""

		cannabis_account_heads = get_account_heads(doc.company)
		for account_head in cannabis_account_heads:
			excise_tax_account = account_head.get("excise_tax_account")
			shipping_account = account_head.get("shipping_charges_account")
			
		for tax in doc.get("taxes"):
			if tax.account_head == shipping_account:
				shipping_charges = tax.amount

		for d in doc.get("items"):

			excise_item = frappe.db.sql("""select enable_cultivation_tax,
				cultivation_tax_type from `tabCompliance Item` where item_code=%s""",
				d.item_code, as_dict=1)[0]

			if not excise_item.enable_cultivation_tax:
				return
			else:
				total_shipping_charges = ((shipping_charges/doc.net_total) * d.price_list_rate)
				excise_tax = excise_tax + ((d.amount * 27) / 100) + total_shipping_charges

		row = doc.append('taxes', {})
		row.category = 'Total'
		row.charge_type = "On Net Total"
		row.add_deduct_tax = "Add"
		row.description = "Excise Tax"
		row.account_head = excise_tax_account
		row.tax_amount = excise_tax
		row.total = doc.total + excise_tax


def get_account_heads(company):
	account_heads =  frappe.get_all("CDFTA Cannabis Taxation Account",
		fields=["cultivation_tax_account", "excise_tax_account", "sales_tax_account", "shipping_charges_account"],
		filters={
			"company":company
		})

	if account_heads:
		return account_heads
	else:
		frappe.throw(_("Please set Cannabis Tax account heads in Compliance Settings for Compnay {0}".format(company)))
	
def convert_to_ounce(item_code, uom, qty):
	"convert any unit into ounce"
	conversion_factor = get_uom_conv_factor(uom, 'Ounce')
	if not conversion_factor:
		frappe.throw(_("Add UOM Conversion Factor for {0} to Ounce").format(uom))
	value = qty * conversion_factor
	return value
