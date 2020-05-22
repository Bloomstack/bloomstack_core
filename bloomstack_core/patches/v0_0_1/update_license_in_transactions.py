import frappe
from frappe.modules.utils import sync_customizations
from bloomstack_core.hook_events.utils import get_default_license


def execute():
	sync_customizations("bloomstack_core")

	sales_orders = frappe.get_all("Sales Order",fields=["customer", "name"])
	sales_invoices = frappe.get_all("Sales Invoice",fields=["customer", "name"])
	delivery_notes = frappe.get_all("Sales Invoice",fields=["customer", "name"])
	quotations = frappe.get_all("Quotation",fields=["party_name", "name", "quotation_to"])
	supplier_quotation = frappe.get_all("Supplier Quotation",fields=["supplier", "name"])
	purchase_orders = frappe.get_all("Purchase Order",fields=["supplier", "name"])
	purchase_invoices = frappe.get_all("Purchase Invoice",fields=["supplier", "name"])
	purchase_receipt = frappe.get_all("Purchase Receipt",fields=["supplier", "name"]) 

	for doc in sales_orders:
		license = get_default_license("Customer", doc.customer)
		if not license:
			continue
		frappe.db.set_value("Sales Order", doc.name, "license", license)
		frappe.db.commit()

	for doc in sales_invoices:
		license = get_default_license("Customer", doc.customer)
		if not license:
			continue
		frappe.db.set_value("Sales Invoice", doc.name, "license", license)
		frappe.db.commit()
	
	for doc in delivery_notes:
		license = get_default_license("Customer", doc.customer)
		if not license:
			continue
		frappe.db.set_value("Delivery Note", doc.name, "license", license)
		frappe.db.commit()

	for doc in quotations:
		if doc.quotation_to == "Customer":
			license = get_default_license("Customer", doc.party_name)
			if not license:
				continue
			frappe.db.set_value("Quotation", doc.name, "license", license)
			frappe.db.commit()

	for doc in supplier_quotation:
		license = get_default_license("Supplier", doc.supplier)
		if not license:
			continue
		frappe.db.set_value("Supplier Quotation", doc.name, "license", license)
		frappe.db.commit()
	
	for doc in purchase_orders:
		license = get_default_license("Supplier", doc.supplier)
		if not license:
			continue
		frappe.db.set_value("Purchase Order", doc.name, "license", license)
		frappe.db.commit()
	
	for doc in purchase_invoices:
		license = get_default_license("Supplier", doc.supplier)
		if not license:
			continue
		frappe.db.set_value("Purchase Invoice", doc.name, "license", license)
		frappe.db.commit()
	
	for doc in purchase_receipt:
		license = get_default_license("Supplier", doc.supplier)
		if not license:
			continue
		frappe.db.set_value("Purchase Receipt", doc.name, "license", license)
		frappe.db.commit()

