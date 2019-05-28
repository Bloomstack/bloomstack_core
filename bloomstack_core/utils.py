from __future__ import unicode_literals

import json

import frappe
from erpnext.stock.doctype.batch.batch import get_batch_qty
from python_metrc import METRC


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


@frappe.whitelist()
def move_expired_batches(source_name, target_doc=None):
	batch_details = get_batch_qty(source_name)
	target_warehouse = frappe.flags.args.get("warehouse")

	item = frappe.db.get_value("Batch", source_name, "item")
	uom = frappe.db.get_value("Item", item, "stock_uom")

	stock_entry = frappe.new_doc("Stock Entry")
	stock_entry.purpose = "Material Transfer"

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

@frappe.whitelist()
def make_authorization_request(source_name, target_doc=None):
	print(locals())

@frappe.whitelist(allow_guest=True)
def authorize_document(sign=None, signee=None, docname=None):
	authorization_request = frappe.get_doc("Authorization Request", docname)
	authorization_request.signature = sign
	authorization_request.signee_name = signee
	authorization_request.status = "Approved"
	authorization_request.flags.ignore_permissions = True
	authorization_request.save()

	authorized_doc = frappe.get_doc(authorization_request.linked_doctype, authorization_request.linked_docname)
	try:
		print("\n try \n")
		if authorized_doc.is_signed == 0:
			authorized_doc.is_signed = 1
			authorized_doc.authorizer_signature = sign
			authorized_doc.signee = signee
			authorized_doc.submit()
	except:
		print("\n except \n")
		authorized_doc.submit()


@frappe.whitelist()
def create_authorization_request(dt, dn, contact_email, contact_name=None):
	print("lllllloooooocals", locals())
	print("Hellooooooooooooo")
	new_authorization_request = frappe.new_doc("Authorization Request")
	new_authorization_request.signee_name = contact_name
	new_authorization_request.linked_doctype = dt
	new_authorization_request.linked_docname = dn
	new_authorization_request.authorizer_email = contact_email
	new_authorization_request.save()
	print("GENERATED")