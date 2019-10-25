import json

import requests

import frappe
from frappe import _
from frappe.utils import get_url


class ClientRegistrationError(frappe.ValidationError): pass


def after_install():
	"""
		After the site is successfully created, we register the company on
		Bloomstack's authentication servers, and create login integrations
		and an OAuth client for the company.
	"""

	client_info = register_client()
	create_social_login_keys(client_info)
	create_oauth_client(client_info)


def register_client():
	site = frappe.local.site
	base_url = frappe.local.conf.get("auth_server")
	company_name = frappe.local.conf.get("company_name")
	redirect_uri = frappe.local.conf.get("oauth_login_redirect_uri")

	redirect_uris = [site + redirect_uri]
	scopes = ["openid", "roles", "email", "profile"]

	url = base_url + "/client/v1/create"
	headers = {
		'Authorization': 'Bearer <token>',
		'Content-Type': 'application/json'
	}
	data = {
		"name": company_name,
		"isTrusted": "0",
		"autoApprove": True,
		"redirectUris": redirect_uris,
		"allowedScopes": scopes,
		"authenticationMethod": "PUBLIC_CLIENT"
	}

	response = requests.post(url, headers=headers, data=json.dumps(data))

	if not response.ok:
		frappe.throw(_("There was a server error while trying to create the site."), exc=ClientRegistrationError)

	client_info = json.loads(response.content)
	return client_info


def create_social_login_keys(client_info):
	# create a login key for Bloomstack, enabled by default
	scopes = " ".join(client_info.get("allowedScopes"))
	response_type = "code"
	auth_url_data = json.dumps(dict(scope=scopes, response_type=response_type))

	bloomstack_social_login_key = frappe.new_doc("Social Login Key")
	bloomstack_social_login_key.update({
		"enable_social_login": True,
		"provider_name": "Bloomstack",
		"client_id": client_info.get("clientId"),
		"client_secret": client_info.get("clientSecret"),
		"base_url": frappe.local.conf.get("auth_server"),
		"authorize_url": frappe.local.conf.get("social_login_authorize_url"),
		"redirect_url": frappe.local.conf.get("oauth_login_redirect_uri"),
		"access_token_url": frappe.local.conf.get("social_login_access_token_url"),
		"api_endpoint": frappe.local.conf.get("social_login_api_endpoint"),
		"auth_url_data": auth_url_data
	})
	bloomstack_social_login_key.insert()

	# create a login key for Frappe, disabled by default
	frappe_social_login_key = frappe.new_doc("Social Login Key")
	frappe_social_login_key.update({
		"enable_social_login": False,
		"provider_name": "Frappe",
		"client_id": None,
		"client_secret": None,
		"base_url": get_url(),
		"authorize_url": "/api/method/frappe.integrations.oauth2.authorize",
		"redirect_url": "/api/method/frappe.www.login.login_via_frappe",
		"access_token_url": "/api/method/frappe.integrations.oauth2.get_token",
		"api_endpoint": "/api/method/frappe.integrations.oauth2.openid_profile",
		"auth_url_data": json.dumps({"scope": "openid", "response_type": "code"})
	})
	frappe_social_login_key.insert()


def create_oauth_client(client_info):
	pass
