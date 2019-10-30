# -*- coding: utf-8 -*-
"""
OAuth 2.0 Client for Frappe Apps
"""

from __future__ import unicode_literals

import base64
import json

import requests
from six.moves.urllib.parse import unquote

import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def callback(code=None, state=None):
	"""
		Callback for handling client's code
	"""

	if frappe.request.method != 'GET':
		throw_error(_('Invalid Method'))
		return

	if frappe.session.user == 'Guest':
		throw_error(_('Please Sign In'))
		return

	path = frappe.request.path[1:].split("/")

	if len(path) == 4 and path[3]:
		connected_app = path[3]
		stored_state = frappe.db.get_value("Token Cache", {
			'user': frappe.session.user,
			'connected_app': connected_app,
			'name': connected_app + '-' + frappe.session.user,
		})

		if not stored_state:
			throw_error(_('State Not Found'))
			return

		stored_state = frappe.get_doc('Token Cache', stored_state)

		payload = json.loads(b64_to_str(state))
		stored_payload = json.loads(b64_to_str(stored_state.state))

		if payload.get('uid') != stored_payload.get('uid'):
			throw_error(_('Invalid State'))
			return

		try:
			app = frappe.get_doc('Connected App', connected_app)
		except frappe.exceptions.DoesNotExistError:
			throw_error(_('Invalid App'))
			return

		data = {
			"client_id": app.client_id,
			"redirect_uri": app.redirect_uri,
			"grant_type": "authorization_code",
			"code": code
		}

		response = requests.post(app.token_endpoint, data=data)
		token = response.json()
		stored_state.access_token = token.get('access_token')
		stored_state.refresh_token = token.get('refresh_token')
		stored_state.expires_in = token.get('expires_in')
		stored_state.state = None
		stored_state.save()
		frappe.db.commit()

		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = payload.get('redirect_to')
	else:
		throw_error(_('Invalid Parameter(s)'))
		return


def throw_error(error):
	"""
		Set Response Status 400 and show error
	"""
	frappe.local.response['http_status_code'] = 400
	frappe.local.response['error'] = error


def str_to_b64(string):
	"""
		Returns base64 encoded string
	"""
	return base64.b64encode(string.encode('utf-8'))


def b64_to_str(b64):
	"""
		Returns base64 decoded string
	"""
	return base64.b64decode(b64).decode('utf-8')
