from urllib.parse import urlparse

import frappe
from bloomstack_core.bloomtrace import get_bloomtrace_client
from frappe.utils import get_url

def update_bloomstack_site_user():
	frappe_client = get_bloomtrace_client()
	if not frappe_client:
			return

	site_url = urlparse(get_url()).netloc
	pending_requests = frappe.get_all("Integration Request", 
		filters={"status": ["IN", ["Queued", "Failed"]], "reference_doctype": "User", "integration_request_service": "BloomTrace"})

	for request in pending_requests:
		integration_request = frappe.get_doc("Integration Request", request.name)
		user = frappe.get_doc("User", integration_request.reference_docname)

		try:
			bloomstack_site_user = frappe_client.get_doc("Bloomstack Site User", filters={
					"bloomstack_site": site_url, 
					"email": user.email
				})

			if not bloomstack_site_user:
				bloomstack_site_user = {
					"doctype": "Bloomstack Site User",
					"enabled": user.enabled,
					"first_name": user.first_name,
					"last_name": user.last_name,
					"email": user.email,
					"bloomstack_site": site_url
				}
				
				frappe_client.insert(bloomstack_site_user)
			else:
				doc_name = bloomstack_site_user[0].get('name')
				bloomstack_site_user = {
					"doctype": "Bloomstack Site User",
					"name": doc_name,
					"enabled": user.enabled,
					"first_name": user.first_name,
					"last_name": user.last_name,
					"email": user.email,
					"bloomstack_site": site_url
				}
				frappe_client.update(bloomstack_site_user)
			integration_request.status = "Completed"
			integration_request.save(ignore_permissions=True)

		except:
			integration_request.status = "Failed"
			integration_request.save(ignore_permissions=True)

