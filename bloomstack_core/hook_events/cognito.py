import frappe
from frappe.utils import cstr, cint

BLOOMSTACK_SOCIAL_LOGIN_NAME = 'Bloomstack'

def setup():
	"""
	Checks if this bloomstack instance has been configured with cognito correctly

	# How to configure

	At a minimum you need to add a "cognito" key in your site_config.json file with the app
	client_id and client_secret:

	```
	{
		... other site_config fields ...
		"cognito": {
			"client_id": "<client id provided by aws>",
			"client_secret": "<client secret provided by aws>"
		}
	}
	```

	## Allowed Fields

	Fields in cognito config match social login fields:

	### client_id (string)
		The client id provided by aws. Find it in your cognito backend.

	### client_secret (string)
		The client secret provided by aws.

	### base_url (string)
		The base authentication server url. Defaults to https://auth.bloomstack.com

	### authorize_url (string)
		The url path on this bloomstack instance to authorize token

	### redirect_url (string)
		The url used by cognito to route users back to this bloomstack instance.
		Defaults to https://<site name>/api/method/frappe.integrations.oauth2_logins.custom/bloomstack

	### access_token_url (string)
		OAuth2 endpoint to retrieve access token

	### api_endpoint (string)
		OAuth2 endpoint to retrieve meta info

	### auth_url_data (string)
		Cognito OAuth access info. Should match what's setup on cognito's backend.
		Defaults to:

		{ "response_type": "code", "scope": "email openid profile" }

	### user_id_property (string)
		The User doctype field OAuth uses to match a cognito account to an internal frappe account.
		Defaults to email field

	### disable (int)
		Set to 1 to dissable cognito social login.
		You can use this temporarily disable cognito login during provisioning if necessary
	"""

	# Find cognito keys on site_config
	config = frappe.conf.get("cognito", False)
	if not config:
		print("Missing cognito configuration on site_config.json")
		return

	print("Updating cognito integration...")
	# Find bloomstack social login key record
	if frappe.db.exists('Social Login Key', BLOOMSTACK_SOCIAL_LOGIN_NAME):
		bloomstack_social_key = frappe.get_doc('Social Login Key', BLOOMSTACK_SOCIAL_LOGIN_NAME)
	else:
		bloomstack_social_key = frappe.new_doc('Social Login Key')
		bloomstack_social_key.provider_name = BLOOMSTACK_SOCIAL_LOGIN_NAME

	site_name = cstr(frappe.local.site)

	# update social key values
	bloomstack_social_key.client_id = config.get("client_id")
	bloomstack_social_key.client_secret = config.get("client_secret")
	bloomstack_social_key.base_url = config.get("base_url", "https://auth.bloomstack.com")
	bloomstack_social_key.authorize_url = config.get("authorize_url", "/oauth2/authorize")
	bloomstack_social_key.redirect_url = config.get("redirect_url", \
		"https://{}/api/method/frappe.integrations.oauth2_logins.custom/bloomstack".format(site_name))
	bloomstack_social_key.access_token_url = config.get("access_token_url", "/oauth2/token")
	bloomstack_social_key.api_endpoint = config.get("api_endpoint", "/oauth2/userInfo")
	bloomstack_social_key.auth_url_data = config.get("auth_url_data", \
		'{ "response_type": "code", "scope": "email openid profile" }')
	bloomstack_social_key.user_id_property = config.get("user_id_property", "email")
	bloomstack_social_key.enable_social_login = 0 if cint(config.get("disable", 0)) == 1 else 1

	if bloomstack_social_key.enable_social_login == 0:
		print("!! Cognito login has been disabled...")

	bloomstack_social_key.save()