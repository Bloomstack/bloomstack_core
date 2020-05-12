from __future__ import unicode_literals
import re
import frappe
from erpnext.shopping_cart.doctype.shopping_cart_settings.shopping_cart_settings import get_shopping_cart_settings
from erpnext import get_default_company
from frappe import _

def get_context(context):
	doctype = frappe.local.request.args.get('doctype')
	name = frappe.local.request.args.get("name")

	if not doctype or not name:
		context.error = "Provided Payment URL is invalid."

	# setup cart context
	shopping_cart_settings = get_shopping_cart_settings()
	context.payment_gateway_list = shopping_cart_settings.gateways
	context.enabled_checkout = shopping_cart_settings.enable_checkout

	if not context.enabled_checkout:
		context.error = "Please enable checkout to continue."

	# setup document context
	context.doc = frappe.get_doc(doctype, name)

	if not frappe.has_website_permission(context.doc):
		frappe.throw(_("Not Permitted"), frappe.PermissionError)


