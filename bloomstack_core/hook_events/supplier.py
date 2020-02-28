import frappe
from erpnext import get_default_company
from erpnext.controllers.status_updater import status_map
from frappe.contacts.doctype.contact.contact import get_default_contact


@frappe.whitelist()
def send_purchase_documents(doctype, supplier, email, status, from_date, to_date):
	filters = {
		"supplier": supplier,
		"status": status
	}

	if doctype == "Purchase Order":
		filters["transaction_date"] = ["between", [from_date, to_date]]
	elif doctype == "Purchase Invoice":
		filters["posting_date"] = ["between", [from_date, to_date]]

	docs = frappe.get_all(doctype, filters=filters)

	if not docs:
		return []

	attachments = [frappe.attach_print(doctype, doc.name) for doc in docs]

	frappe.sendmail(
		recipients=email,
		subject="View your {0}s with {1}".format(doctype, get_default_company()),
		attachments=attachments
	)

	return docs


@frappe.whitelist()
def get_supplier_emails(supplier):
	contact_emails = []

	contacts = frappe.get_all("Contact",
		filters=[
			["Dynamic Link", "link_doctype", "=", "Supplier"],
			["Dynamic Link", "link_name", "=", supplier],
		])

	for contact in contacts:
		contact_doc = frappe.get_doc("Contact", contact.name)

		for email in contact_doc.email_ids:
			contact_emails.append({
				"email": email.email_id,
				"is_primary": email.is_primary
			})

	return {
		"contact_emails": contact_emails
	}
