import frappe
from frappe.frappeclient import FrappeClient, AuthError


def get_bloomtrace_client():
	url = frappe.conf.get("bloomtrace_server")
	username = frappe.conf.get("bloomtrace_username")
	password = frappe.conf.get("bloomtrace_password")

	if not url:
		return
	
	try:
		client = FrappeClient(url, username=username, password=password, verify=True)
	except ConnectionError:
		return
	except AuthError:
		return

	return client
