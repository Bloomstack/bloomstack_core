import frappe
from frappe.modules.utils import sync_customizations


def execute():
	frappe.reload_doc('bloomstack_core', 'doctype', 'compliance_license_detail', force=True)
	frappe.reload_doc('selling', 'doctype', 'customer', force=True)
	frappe.reload_doc('setup', 'doctype', 'company', force=True)
	frappe.reload_doc('buying', 'doctype', 'supplier', force=True)
	sync_customizations("bloomstack_core")

	customers = frappe.get_all("Customer")
	for customer in customers:
		customer_doc = frappe.get_doc("Customer", customer.name)
		if customer_doc.license:
			customer_doc.append("licenses", {
				"license": customer_doc.license,
				"is_default": 1
			})
			customer_doc.save()

	suppliers = frappe.get_all("Supplier")
	for supplier in suppliers:
		supplier_doc = frappe.get_doc("Supplier", supplier.name)
		if supplier_doc.license:
			supplier_doc.append("licenses", {
				"license": supplier_doc.license,
				"is_default": 1
			})
			supplier_doc.save()

	companies = frappe.get_all("Company")
	for company in companies:
		company_doc = frappe.get_doc("Company", company.name)
		if company_doc.license:
			company_doc.append("licenses", {
				"license": company_doc.license,
				"is_default": 1
			})
			company_doc.save()
