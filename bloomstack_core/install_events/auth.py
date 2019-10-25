import json

import requests

import frappe
from frappe import _
from frappe.utils import get_url

FRAPPE_SITE_BASE_URL = get_url()
FRAPPE_AUTHORIZE_URL = "/api/method/frappe.integrations.oauth2.authorize"
FRAPPE_REDIRECT_URL = "/api/method/frappe.www.login.login_via_frappe"
FRAPPE_ACCESS_TOKEN_URL = "/api/method/frappe.integrations.oauth2.get_token"
FRAPPE_PROFILE_URL = "/api/method/frappe.integrations.oauth2.openid_profile"
FRAPPE_REVOKATION_URL = "/api/method/frappe.integrations.oauth2.revoke_token"


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
	create_oauth_client(auth_client_info)
	frappe_client_info = register_frappe_client(auth_client_info)


def register_auth_client():
	auth_base_url = frappe.local.conf.get("auth_server")
	company_name = frappe.local.conf.get("company_name")
	redirect_uri = frappe.local.conf.get("oauth_login_redirect_uri")

	redirect_uris = [FRAPPE_SITE_BASE_URL + redirect_uri]
	scopes = ["openid", "roles", "email", "profile"]

	url = auth_base_url + "/client/v1/create"
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
	frappe_social_login_key.update({
		"enable_social_login": False,
		"provider_name": "Frappe",
		"client_id": None,
		"client_secret": None,
		"base_url": FRAPPE_SITE_BASE_URL,
		"authorize_url": FRAPPE_AUTHORIZE_URL,
		"redirect_url": FRAPPE_REDIRECT_URL,
		"access_token_url": FRAPPE_ACCESS_TOKEN_URL,
		"api_endpoint": FRAPPE_PROFILE_URL,
		"auth_url_data": json.dumps({"scope": "openid", "response_type": "code"})
	})
	frappe_social_login_key.insert()


def create_oauth_client(client_info):
	scopes = " ".join(client_info.get("allowedScopes"))
	redirect_uris = client_info.get("redirectUris")

	if not redirect_uris:
		return

	oauth_client = frappe.new_doc("OAuth Client")
	oauth_client.update({
		"client_id": client_info.get("clientId"),
		"client_secret": client_info.get("clientSecret"),
		"app_name": frappe.local.conf.get("company_name"),
		"skip_authorization": True,
		"scopes": str(scopes),
		"redirect_uris": str("\n".join(redirect_uris)),
		"default_redirect_uri": redirect_uris[0]
	})
	oauth_client.insert()


def register_frappe_client(client_info):
	scopes = client_info.get("allowedScopes")
	frappe_base_url = frappe.local.conf.get("frappe_server")
	company_name = frappe.local.conf.get("company_name")

	url = frappe_base_url + "/frappe/v1/connect_client"
	headers = {
		'Authorization': 'Bearer <token>',
		'Content-Type': 'application/json'
	}
	data = {
		"name": company_name,
		"clientId": client_info.get("clientId"),
		"clientSecret": client_info.get("clientSecret"),
		"authServerURL": FRAPPE_SITE_BASE_URL,
		"profileURL": FRAPPE_SITE_BASE_URL + FRAPPE_PROFILE_URL,
		"tokenURL": FRAPPE_SITE_BASE_URL + FRAPPE_ACCESS_TOKEN_URL,
		"authorizationURL": FRAPPE_SITE_BASE_URL + FRAPPE_AUTHORIZE_URL,
		"revocationURL": FRAPPE_SITE_BASE_URL + FRAPPE_REVOKATION_URL,
		"scope": scopes
	}

	response = requests.post(url, headers=headers, data=json.dumps(data))

	if not response.ok:
		frappe.throw(_("There was a server error while trying to create the site"), exc=FrappeClientRegistrationError)

	client_info = response.json()
	return client_info
