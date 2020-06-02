from __future__ import unicode_literals

import json

from python_metrc import METRC
from six import string_types

import frappe
from erpnext import get_default_company
from erpnext.stock.doctype.batch.batch import get_batch_qty
from frappe.utils import get_url, today


def welcome_email():
	return "Welcome to Bloomstack"


@frappe.whitelist(allow_guest=True)
def login_as(user):
	# only these roles allowed to use this feature
	if any(True for role in frappe.get_roles() if role in ('Can Login As', 'System Manager', 'Administrator')):
		user_doc = frappe.get_doc("User", user)

		# only administrator can login as a system user
		if not("Administrator" in frappe.get_roles()) and user_doc and user_doc.user_type == "System User":
			return False

		frappe.local.login_manager.login_as(user)
		frappe.set_user(user)

		frappe.db.commit()
		frappe.local.response["redirect_to"] = '/'
		return True

	return False


def get_abbr(txt, max_length=2):
	"""
		Extract abbreviation from the given string as:
			- Single-word strings abbreviate to the letters of the string, upto the max length
			- Multi-word strings abbreviate to the initials of each word, upto the max length

	Args:
		txt (str): The string to abbreviate
		max_length (int, optional): The max length of the abbreviation. Defaults to 2.

	Returns:
		str: The abbreviated string, in uppercase
	"""

	if not txt:
		return

	if not isinstance(txt, string_types):
		try:
			txt = str(txt)
		except:
			return

	abbr = ""
	words = txt.split(" ")

	if len(words) > 1:
		for word in words:
			if len(abbr) >= max_length:
				break

			if word.strip():
				abbr += word.strip()[0]
	else:
		abbr = txt[:max_length]

	abbr = abbr.upper()
	return abbr


@frappe.whitelist()
def move_expired_batches(source_name, target_doc=None):
	batch_details = get_batch_qty(source_name)
	target_warehouse = frappe.flags.args.get("warehouse")

	item = frappe.db.get_value("Batch", source_name, "item")
	uom = frappe.db.get_value("Item", item, "stock_uom")

	stock_entry = frappe.new_doc("Stock Entry")
	stock_entry.stock_entry_type = "Material Transfer"

	for batch in batch_details:
		if batch.get("qty") > 0:
			stock_entry.append("items", {
				"item_code": item,
				"qty": batch.get("qty"),
				"uom": uom,
				"stock_uom": uom,
				"batch_no": source_name,
				"s_warehouse": batch.get("warehouse"),
				"t_warehouse": target_warehouse
			})

	return stock_entry


def get_metrc():
	settings = frappe.get_single("Compliance Settings")

	if not settings.is_compliance_enabled:
		return

	if not all([settings.metrc_url, settings.metrc_vendor_key, settings.metrc_user_key, settings.metrc_vendor_key]):
		frappe.throw("Please configure Compliance Settings")

	return METRC(settings.metrc_url, settings.get_password("metrc_vendor_key"), settings.get_password("metrc_user_key"), settings.metrc_license_no)


def log_request(endpoint, request_data, response, ref_dt=None, ref_dn=None):
	request = frappe.new_doc("API Request Log")
	request.update({
		"endpoint": endpoint,
		"request_body": json.dumps(request_data, indent=4, sort_keys=True),
		"response_code": response.status_code,
		"response_body": json.dumps(response.text, indent=4, sort_keys=True),
		"reference_doctype": ref_dt,
		"reference_document": ref_dn
	})
	request.insert()
	frappe.db.commit()


def email_authorized_doc(authorization_request_name):
	authorization_request = frappe.get_doc("Authorization Request", authorization_request_name)
	authorized_doc = frappe.get_doc(authorization_request.linked_doctype, authorization_request.linked_docname)
	recipients = [authorization_request.authorizer_email]
	company = authorized_doc.company if hasattr(authorized_doc, 'company') else get_default_company()
	subject = "Your signed {0} with {1}".format(authorized_doc.doctype, company)
	message = frappe.render_template("templates/emails/authorization_request.html", {
			"authorization_request": authorization_request,
			"company": company
		})
	print_format = "Bloomstack Contract" if authorized_doc.doctype == 'Contract' else "Standard"
	attachments = [frappe.attach_print(authorized_doc.doctype, authorized_doc.name, print_format=print_format)]
	frappe.sendmail(recipients=recipients, attachments=attachments, subject=subject, message=message)


@frappe.whitelist()
def create_contract_from_quotation(source_name, target_doc=None):
	existing_contract = frappe.db.exists("Contract", {"document_type": "Quotation", "document_name": source_name})
	if existing_contract:
		contract_link = frappe.utils.get_link_to_form("Contract", existing_contract)
		frappe.throw("A Contract already exists for this Quotation at {0}".format(contract_link))

	contract = frappe.new_doc("Contract")
	contract.party_name = frappe.db.get_value("Quotation", source_name, "party_name")
	contract.document_type = "Quotation"
	contract.document_name = source_name
	return contract


@frappe.whitelist()
def create_customer(source_name, target_doc=None):
	existing_customers = get_existing_licensees(source_name, "Customer")
	if existing_customers:
		customer_link = frappe.utils.get_link_to_form("Customer", existing_customers[0])
		frappe.throw("A Customer already exists for this license - {0}".format(customer_link))

	customer = frappe.new_doc("Customer")
	customer.customer_name = frappe.db.get_value("Compliance Info", source_name, "legal_name")
	customer.append("licenses", {
		"license": source_name,
		"is_default": 1
	})

	return customer


@frappe.whitelist()
def create_supplier(source_name, target_doc=None):
	existing_suppliers = get_existing_licensees(source_name, "Supplier")
	if existing_suppliers:
		supplier_link = frappe.utils.get_link_to_form("Supplier", existing_suppliers[0])
		frappe.throw("A Supplier already exists for this license - {0}".format(supplier_link))

	supplier = frappe.new_doc("Supplier")
	supplier.supplier_name = frappe.db.get_value("Compliance Info", source_name, "legal_name")
	supplier.append("licenses", {
		"license": source_name,
		"is_default": 1
	})

	return supplier


def get_existing_licensees(license, party_type):
	existing_licensees = frappe.get_all("Compliance License Detail",
		filters={"license": license, "parenttype": party_type},
		fields=["parent"],
		distinct=True)

	existing_licensees = [license.parent for license in existing_licensees if license.parent]
	return existing_licensees


@frappe.whitelist(allow_guest=True)
def authorize_document(sign=None, signee=None, docname=None):
	if frappe.db.exists("Authorization Request", docname):
		authorization_request = frappe.get_doc("Authorization Request", docname)
		authorization_request.signature = sign
		authorization_request.signee_name = signee
		authorization_request.status = "Approved"
		authorization_request.flags.ignore_permissions = True
		authorization_request.save()

		authorized_doc = frappe.get_doc(authorization_request.linked_doctype, authorization_request.linked_docname)
		if hasattr(authorized_doc, "is_signed") and hasattr(authorized_doc, "customer_signature") and hasattr(authorized_doc, "signee"):
			if authorized_doc.is_signed == 0:
				authorized_doc.is_signed = 1
				authorized_doc.customer_signature = sign
				authorized_doc.signee = signee
				authorized_doc.signed_on = frappe.utils.now()

		authorized_doc.flags.ignore_permissions = True
		authorized_doc.submit()

		email_authorized_doc(docname)


@frappe.whitelist(allow_guest=True)
def reject_document(docname):
	if frappe.db.exists("Authorization Request", docname):
		authorization_request = frappe.get_doc("Authorization Request", docname)
		authorization_request.status = "Rejected"
		authorization_request.save()


@frappe.whitelist()
def create_authorization_request(dt, dn, contact_email, contact_name):
	new_authorization_request = frappe.new_doc("Authorization Request")
	new_authorization_request.linked_doctype = dt
	new_authorization_request.linked_docname = dn
	new_authorization_request.authorizer_email = contact_email
	new_authorization_request.authorizer_name = contact_name
	new_authorization_request.save()

@frappe.whitelist()
def get_contact(doctype, name, contact_field):

	contact = frappe.db.get_value(doctype, name, contact_field)

	contact_persons = frappe.db.sql(
		"""
			SELECT parent,
				(SELECT is_primary_contact FROM tabContact c WHERE c.name = dl.parent) AS is_primary_contact
			FROM
				`tabDynamic Link` dl
			WHERE
				dl.link_doctype=%s
				AND dl.link_name=%s
				AND dl.parenttype = "Contact"
		""", (frappe.unscrub(contact_field), contact), as_dict=1)

	if contact_persons:
		for contact_person in contact_persons:
			contact_person.email_id = frappe.db.get_value("Contact", contact_person.parent, ["email_id"])
			if contact_person.is_primary_contact:
				return contact_person

		contact_person = contact_persons[0]

		return contact_person


@frappe.whitelist()
def get_document_links(doctype, docs):
	docs = json.loads(docs)
	print_format = "print_format"
	links = []
	for doc in docs:
		link = frappe.get_template("templates/emails/print_link.html").render({
			"url": get_url(),
			"doctype": doctype,
			"name": doc.get("name"),
			"print_format": print_format,
			"key": frappe.get_doc(doctype, doc.get("name")).get_signature()
		})
		links.append(link)
	return links


@frappe.whitelist()
def link_address_or_contact(ref_doctype, ref_name, link_doctype, link_name):
	doc = frappe.get_doc(ref_doctype, ref_name)
	doc.append("links", {"link_doctype": link_doctype, "link_name": link_name})
	doc.save()


@frappe.whitelist()
def unlink_address_or_contact(ref_doctype, ref_name, doctype, name):
	doc = frappe.get_doc(ref_doctype, ref_name)
	links = doc.get("links")
	for data in links:
		if data.link_doctype == doctype and data.link_name == name:
			links.remove(data)
	doc.save()


@frappe.whitelist()
def delete_address_or_contact(ref_doctype, ref_name, doctype, name):
	doc = frappe.get_doc(ref_doctype, ref_name)
	links = doc.get("links")
	if len(links) > 1:
		unlink_address_or_contact(ref_doctype, ref_name, doctype, name)
	else:
		frappe.delete_doc(ref_doctype, ref_name)


def get_active_licenses(doctype, txt, searchfield, start, page_len, filters):
	return frappe.get_all(doctype,
		filters=[
			[doctype, "status", "!=", "Expired"],
			[doctype, "name", "NOT IN", filters.get("set_licenses")],
			[doctype, "name", "like", "%{0}%".format(txt)]
		],
		or_filters=[
			{"license_expiry_date": ["is", "not set"]},
			{"license_expiry_date": [">=", today()]}
		],
		fields=["name", "legal_name", "license_number", "status", "license_issuer",
			"license_for", "license_expiry_date", "license_type"],
		as_list=True)
