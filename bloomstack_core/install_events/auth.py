import json

import requests

import frappe


def after_install():
	create_client()


def create_client():
	site = frappe.local.site
	base_url = frappe.local.conf.get("auth_server")
	company_name = frappe.local.conf.get("company_name")

	redirect_uris = [site + "/api/method/frappe.integrations.oauth2_logins.custom/bloomstack"]
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

	result = requests.post(url, headers=headers, data=json.dumps(data))

	"""
	result = {
		"name": "company_name",
		"isTrusted": "0",
		"autoApprove": true,
		"redirectUris": [site + "/api/method/frappe.integrations.oauth2_logins.custom/bloomstack"],
		"allowedScopes": ["openid", "roles", "email", "profile"],
		"authenticationMethod": "PUBLIC_CLIENT",
		"createdBy": "<userID",
		"modifiedBy": "<userID",
		"creation": "2019-10-24T13:18:09.959Z",
		"modified": "2019-10-24T13:18:09.959Z",
		"clientId": "<clientID>",
		"clientSecret": "<clientSecret>"
	}
	"""

	# TODO:
	# 1) Handle social login keys creation
	# 2) Handle OAuth Client creation
