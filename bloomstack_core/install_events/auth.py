import json

import requests

import frappe
from erpnext import get_default_company
from frappe import _
from frappe.utils import get_url

COMPANY_NAME = get_default_company()
FRAPPE_SITE_BASE_URL = get_url()
FRAPPE_AUTHORIZE_ENDPOINT = "/api/method/frappe.integrations.oauth2.authorize"
FRAPPE_ACCESS_TOKEN_ENDPOINT = "/api/method/frappe.integrations.oauth2.get_token"
FRAPPE_PROFILE_ENDPOINT = "/api/method/frappe.integrations.oauth2.openid_profile"
FRAPPE_REVOKATION_ENDPOINT = "/api/method/frappe.integrations.oauth2.revoke_token"


class AuthClientRegistrationError(frappe.ValidationError): pass
class FrappeClientRegistrationError(frappe.ValidationError): pass


def after_install():
	"""
		After the site is successfully created, we register the company on
		Bloomstack's authentication servers, and create login integrations
		and an OAuth client for the company.
	"""

	auth_client_info = register_auth_client()
	create_social_login_keys(auth_client_info)

	oauth_client_info = create_oauth_client()
	register_frappe_client(oauth_client_info)


def register_auth_client():
	auth_base_url = frappe.local.conf.get("auth_server")
	redirect_uri = frappe.local.conf.get("oauth_login_redirect_uri")
	redirect_uris = [FRAPPE_SITE_BASE_URL + redirect_uri]
	scopes = ["openid", "roles", "email", "profile"]

	url = auth_base_url + "/client/v1/create"
	headers = {
		'Authorization': 'Bearer <token>',
		'Content-Type': 'application/json'
	}
	data = {
		"name": COMPANY_NAME,
		"isTrusted": "0",
		"autoApprove": True,
		"redirectUris": redirect_uris,
		"allowedScopes": scopes,
		"authenticationMethod": "PUBLIC_CLIENT"
	}

	response = requests.post(url, headers=headers, data=json.dumps(data))

	if not response.ok:
		frappe.throw(_("There was a server error while trying to create the site"), exc=AuthClientRegistrationError)

	client_info = response.json()
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
	frappe_social_login_key.get_social_login_provider("Frappe", initialize=True)
	frappe_social_login_key.enable_social_login = False
	frappe_social_login_key.custom_base_url = False
	frappe_social_login_key.base_url = FRAPPE_SITE_BASE_URL
	frappe_social_login_key.insert()


def create_oauth_client():
	oauth_client = frappe.new_doc("OAuth Client")
	oauth_client.update({
		"app_name": get_default_company(),
		"skip_authorization": True,
		"scopes": "all openid",
		"redirect_uris": frappe.local.conf.get("frappe_server") + "/frappe/callback",
		"default_redirect_uri": frappe.local.conf.get("frappe_server") + "/frappe/callback"
	})
	oauth_client.insert()
	return oauth_client


def register_frappe_client(client_info):
	frappe_base_url = frappe.local.conf.get("frappe_server")

	url = frappe_base_url + "/frappe/v1/connect_client"
	headers = {
		'Authorization': 'Bearer <token>',
		'Content-Type': 'application/json'
	}
	data = {
		"name": COMPANY_NAME,
		"clientId": client_info.client_id,
		"clientSecret": client_info.client_secret,
		"authServerURL": FRAPPE_SITE_BASE_URL,
		"profileURL": FRAPPE_SITE_BASE_URL + FRAPPE_PROFILE_ENDPOINT,
		"tokenURL": FRAPPE_SITE_BASE_URL + FRAPPE_ACCESS_TOKEN_ENDPOINT,
		"authorizationURL": FRAPPE_SITE_BASE_URL + FRAPPE_AUTHORIZE_ENDPOINT,
		"revocationURL": FRAPPE_SITE_BASE_URL + FRAPPE_REVOKATION_ENDPOINT,
		"scope": client_info.scopes.split(" ")
	}

	response = requests.post(url, headers=headers, data=json.dumps(data))

	if not response.ok:
		frappe.throw(_("There was a server error while trying to create the site"), exc=FrappeClientRegistrationError)
