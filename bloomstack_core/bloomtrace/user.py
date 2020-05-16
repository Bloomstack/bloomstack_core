from urllib.parse import urlparse

import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import get_url

def update_bloomtrace_client_user():
	client = get_bloomtrace_client()
	if not client:
			return

	site_url = urlparse(get_url()).netloc

	pending_requests = frappe.get_all("Integration Request", 
		filters={"status": ["IN", ["Queued", "Failed"]], "integration_request_service": "BloomTrace"})

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		user = frappe.get_doc("User", integration_request.reference_docname)
			
		try:
			client_records = client.get_doc("Client", filters={"bloomstack_instance": site_url})
			if not client_records:
				return
			
			client_name = client_records[0].get("name")

			client_user = client.get_doc("Client User", filters={"client": client_name, "email": user.email})

			if not client_user:
				client_user = {
					"doctype": "Client User",
					"enabled": user.enabled,
					"first_name": user.first_name,
					"last_name": user.last_name,
					"email": user.email,
					"client": client_name
				}
				client.insert(client_user)
			else:
				client_user = client_user[0]
				client_user.update({
					"doctype": "Client User",
					"enabled": user.enabled,
					"first_name": user.first_name,
					"last_name": user.last_name,
					"email": user.email,
					"client": client_name
				})
				client.update(client_user)

			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)

		except:
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)
