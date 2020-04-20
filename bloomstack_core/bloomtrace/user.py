from urllib.parse import urlparse

import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import get_url


def create_bloomtrace_client_user(user, method):
	client = get_bloomtrace_client()

	if not client:
		return

	if method == "after_insert":
		site_url = urlparse(get_url()).netloc
		client_records = client.get_doc("Client", filters={"bloomstack_instance": site_url})

		if not client_records:
			return

		client_name = client_records[0].get("name")

		client_user = {
			"doctype": "Client User",
			"enabled": True,
			"first_name": user.first_name,
			"last_name": user.last_name,
			"email": user.email,
			"client": client_name,
			# "user_api_key": ""  Enter METRC User API key here
		}

		client.insert(client_user)
