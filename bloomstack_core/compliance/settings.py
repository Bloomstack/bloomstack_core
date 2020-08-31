import frappe
from bloomstack_core.compliance.utils import get_metrc
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
	enqueue(pull_metrc_item_categories)
	enqueue(pull_metrc_uoms)


def pull_metrc_item_categories():
	"""
	Pull METRC Item categories into Bloomstack.
	"""

	metrc = get_metrc()

	if not metrc:
		return

	response = metrc.items.categories.get()

	# Create root METRC item group
	if not frappe.db.exists("Item Group", "METRC Categories"):
		item_group = frappe.new_doc("Item Group")
		item_group.update({
			"item_group_name": "METRC Categories",
			"parent_item_group": get_root_of("Item Group"),
			"is_group": 1
		})
		item_group.insert()

	for category in response.json():
		# Create Item Group for the METRC category
		if not frappe.db.exists("Item Group", category.get("Name")):
			item_group = frappe.new_doc("Item Group")
			item_group.update({
				"item_group_name": category.get("Name"),
				"parent_item_group": "METRC Categories"
			})
			# Item groups cannot be the same name as an Item
			try:
				item_group.insert()
			except frappe.NameError:
				continue
		else:
			item_group = frappe.get_doc("Item Group", category.get("Name"))

		# Create METRC Item Category
		if frappe.db.exists("Compliance Item Category", category.get("Name")):
			doc = frappe.get_doc("Compliance Item Category", category.get("Name"))
		else:
			doc = frappe.new_doc("Compliance Item Category")

		mandatory_unit = None

		if category.get("RequiresUnitVolume"):
			mandatory_unit = "Volume"
		elif category.get("RequiresUnitWeight"):
			mandatory_unit = "Weight"

		doc.update({
			"category_name": category.get("Name"),
			"item_group": item_group.name,
			"product_category_type": category.get("ProductCategoryType"),
			"quantity_type": category.get("QuantityType"),
			"mandatory_unit": mandatory_unit,
			"strain_mandatory": category.get("RequiresStrain")
		}).save()


def pull_metrc_uoms():
	"""
	Pull METRC Item UOMs into Bloomstack.
	"""

	metrc = get_metrc()

	if not metrc:
		return

	response = metrc.unitsofmeasure.active.get()

	for uom in response.json():
		if frappe.db.exists("Compliance UOM", uom.get("Name")):
			metrc_uom = frappe.get_doc("Compliance UOM", uom.get("Name"))
		else:
			metrc_uom = frappe.new_doc("Compliance UOM")

		metrc_uom.update({
			"uom_name": uom.get("Name"),
			"uom": METRC_UOMS.get(uom.get("Name")),
			"abbreviation": uom.get("Abbreviation"),
			"quantity_type": uom.get("QuantityType")
		}).save()
