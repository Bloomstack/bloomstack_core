import frappe
from bloomstack_core.bloomtrace.utils import get_bloomtrace_client
from frappe.utils.background_jobs import enqueue
from frappe.utils.nestedset import get_root_of

METRC_UOMS = {
	"Each": "Each",
	"Fluid Ounces": "Fluid Ounce (US)",
	"Gallons": "Gallon Liquid (US)",
	"Grams": "Gram",
	"Kilograms": "Kg",
	"Liters": "Litre",
	"Milligrams": "Milligram",
	"Milliliters": "Millilitre",
	"Ounces": "Ounce",
	"Pints": "Pint, Liquid (US)",
	"Pounds": "Pound",
	"Quarts": "Quart Liquid (US)"
}


@frappe.whitelist()
def sync_data():
	enqueue(pull_item_categories_from_bloomtrace)
	enqueue(pull_uoms_from_bloomtrace)


def pull_item_categories_from_bloomtrace():
	"""
	Pull METRC Item categories into Bloomstack from Bloomtrace.
	"""

	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	categories = frappe_client.get_list("Compliance Item Category", fields=["*"])

	create_root_element_if_not_exists()

	for category in categories:
		# Create Item Group for the METRC category
		if not frappe.db.exists("Item Group", category.get("name")):
			item_group = frappe.get_doc({
				"doctype": "Item Group",
				"item_group_name": category.get("name"),
				"parent_item_group": "METRC Categories"
			})
			# Item groups cannot be the same name as an Item
			try:
				item_group.insert()
			except frappe.NameError:
				continue
		else:
			item_group = frappe.get_doc("Item Group", category.get("name"))

		# Create METRC Item Category
		if frappe.db.exists("Compliance Item Category", category.get("name")):
			doc = frappe.get_doc("Compliance Item Category", category.get("name"))
		else:
			doc = frappe.new_doc("Compliance Item Category")

		doc.update({
			"category_name": category.get("name"),
			"item_group": item_group.name,
			"product_category_type": category.get("product_category_type"),
			"quantity_type": category.get("quantity_type"),
			"mandatory_unit": category.get("mandatory_unit"),
			"strain_mandatory": category.get("strain_mandatory")
		}).save()


def pull_uoms_from_bloomtrace():
	"""
	Pull METRC Item UOMs into Bloomstack from Bloomtrace.
	"""

	frappe_client = get_bloomtrace_client()
	if not frappe_client:
		return

	uoms = frappe_client.get_list("Compliance UOM", fields=["*"])

	for uom in uoms:
		if frappe.db.exists("Compliance UOM", uom.get("name")):
			metrc_uom = frappe.get_doc("Compliance UOM", uom.get("name"))
		else:
			metrc_uom = frappe.new_doc("Compliance UOM")

		metrc_uom.update({
			"uom_name": uom.get("name"),
			"uom": METRC_UOMS.get(uom.get("name")),
			"abbreviation": uom.get("abbreviation"),
			"quantity_type": uom.get("quantity_type")
		}).save()


def create_root_element_if_not_exists():
	# Create root METRC item group
	if not frappe.db.exists("Item Group", "METRC Categories"):
		item_group = frappe.get_doc({
			"doctype": "Item Group",
			"item_group_name": "METRC Categories",
			"parent_item_group": get_root_of("Item Group"),
			"is_group": 1
		}).insert()
