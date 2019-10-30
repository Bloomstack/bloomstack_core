# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import json
from datetime import datetime, timedelta

import requests

import frappe
from bloomstack_core.oauth2 import str_to_b64
from frappe.model.document import Document


class ConnectedApp(Document):
	def autoname(self):
		self.callback = frappe.scrub(self.provider_name)

	def validate(self):
		self.generate_redirect_uri()

	def generate_redirect_uri(self):
		redirect_uri = frappe.request.host_url
		redirect_uri += 'api/method/oauth2_client.callback/'
		redirect_uri += self.callback
		self.redirect_uri = redirect_uri

	def get_client_token(self):
		try:
			token = self.get_stored_client_token()
		except frappe.exceptions.DoesNotExistError:
			token = self.retrieve_client_token()
		token = self.check_validity(token)
		return token

	def get_stored_client_token(self):
		token = frappe.get_doc('Token Cache', self.name + '-user')
		return token

	def get_stored_user_token(self, user):
		token = frappe.get_doc('Token Cache', self.name + '-' + user)
		return token

	def retrieve_client_token(self):
		client_secret = frappe.utils.password.get_decrypted_password(
			'Connected App',
			self.name,
			fieldname='client_secret',
			raise_exception=False)
		data = {
			"client_id": self.client_id,
			"client_secret": client_secret,
			"redirect_uri": self.redirect_uri,
			"grant_type": "client_credentials",
			"scope": self.scope.replace(' ', '%20')
		}
		response = requests.post(self.token_endpoint, data=data)
		token = response.json()
		out = self.update_stored_client_token(token)
		return out

	def check_validity(self, token):
		if(token.get('__islocal') or not token.access_token):
			raise frappe.exceptions.DoesNotExistError
		expiry = token.modified + timedelta(seconds=token.expires_in)
		if expiry > datetime.now():
			return token
		return self.refresh_token(token)

	def initiate_auth_code_flow(self, user=None, redirect_to=None):
		if not redirect_to:
			redirect_to = '/desk'

		if not user:
			user = frappe.session.user

		uid = frappe.generate_hash()
		payload = {
			'uid': uid,
			'redirect_to': redirect_to,
		}
		state = str_to_b64(json.dumps(payload))

		try:
			token = frappe.get_doc('Token Cache', self.name + '-' + user)
		except frappe.exceptions.DoesNotExistError:
			token = frappe.new_doc('Token Cache')
			token.user = user
			token.connected_app = self.name

		token.state = state
		token.save()
		frappe.db.commit()

		redirect_to = self.authorization_endpoint
		redirect_to += '?client_id=' + self.client_id
		redirect_to += '&redirect_uri=' + self.redirect_uri
		redirect_to += '&scope=' + self.scope.replace(' ', '%20')
		redirect_to += '&response_type=code'
		redirect_to += '&state=' + state.decode('utf-8')
		return redirect_to

	def get_user_token(self, user=None, redirect_to=None):
		if not user:
			user = frappe.session.user
		try:
			token = self.get_stored_user_token(user)
			token = self.check_validity(token)
		except frappe.exceptions.DoesNotExistError:
			redirect = self.initiate_auth_code_flow(user, redirect_to)
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = redirect
			return redirect
		return token

	def refresh_token(self, token):
		data = {
			"grant_type": "refresh_token",
			"refresh_token": token.refresh_token,
			"client_id": self.client_id,
			"redirect_uri": self.redirect_uri,
			"scope": self.scope.replace(' ', '%20')
		}
		response = requests.post(self.token_endpoint, data=data)
		new_token = response.json()
		token_doc = self.update_stored_client_token(new_token)

		# Revoke old token
		data = {'token': token.get('access_token')}
		headers = token_doc.get_auth_header()
		requests.post(self.revocation_endpoint, data=data, headers=headers)

		return token_doc

	def update_stored_client_token(self, token_data):
		try:
			stored_token = frappe.get_doc('Token Cache', self.name + '-user')
		except frappe.exceptions.DoesNotExistError:
			stored_token = frappe.new_doc('Token Cache')

		stored_token.connected_app = self.name
		stored_token.access_token = token_data.get('access_token')
		stored_token.refresh_token = token_data.get('refresh_token')
		stored_token.expires_in = token_data.get('expires_in')
		stored_token.save(ignore_permissions=True)
		frappe.db.commit()

		return frappe.get_doc('Token Cache', stored_token.name)
