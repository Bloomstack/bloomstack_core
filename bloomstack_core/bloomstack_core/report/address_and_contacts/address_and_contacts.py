# Copyright (c) 2019, Bloom Stack and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from six import iteritems
from six.moves import range

import frappe
from bloomstack_core.hook_events.utils import get_default_license

field_map = {
	"Contact": ["first_name", "last_name", "phone", "mobile_no", "email_id", "is_primary_contact"],
	"Address": ["address_line1", "address_line2", "city", "state", "pincode", "country", "is_primary_address"]
}


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data


def get_party_group(party_type):
	if not party_type:
		return

	group = {
		"Customer": "customer_group",
		"Supplier": "supplier_group",
		"Sales Partner": "partner_type"
	}

	return group[party_type]


def get_columns(filters):
	party_type = filters.get("party_type")
	party_group = get_party_group(party_type)

	columns = [
		"{0}:Link/{0}".format(party_type),
		"{0}::150".format(frappe.unscrub(str(party_group)))
	]

	if party_type == "Customer":
		columns.extend([
			"Territory",
			"Sales Partner"
		])

	if party_type in ("Customer", "Supplier"):
		columns.extend([
			"License Type",
			"License Number"
		])

	columns.extend([
		"Address Line 1",
		"Address Line 2",
		"City",
		"State",
		"Postal Code",
		"Country",
		"Is Primary Address:Check",
		"First Name",
		"Last Name",
		"Phone",
		"Mobile No",
		"Email Id",
		"Is Primary Contact:Check"
	])

	return columns


def get_data(filters):
	party_type = filters.get("party_type")
	party = filters.get("party_name")
	party_group = get_party_group(party_type)

	return get_party_addresses_and_contact(party_type, party, party_group)


def get_party_details(party_type, party_list, party_details):
	for doctype in ("Contact", "Address"):
		filters = [
			["Dynamic Link", "link_doctype", "=", party_type],
			["Dynamic Link", "link_name", "in", party_list]
		]
		fields = ["`tabDynamic Link`.link_name"] + field_map.get(doctype, [])

		records = frappe.get_list(doctype, filters=filters, fields=fields, as_list=True)

		for d in records:
			details = party_details.get(d[0])
			details.setdefault(frappe.scrub(doctype), []).append(d[1:])

	return party_details


def add_blank_columns_for(doctype):
	return [None for field in field_map.get(doctype, [])]


def get_party_addresses_and_contact(party_type, party, party_group):
	data = []

	# Build party details
	party_details = frappe._dict()

	if not party_type:
		return []

	filters = {"name": party} if party else None

	party_list = frappe.get_list(party_type, filters=filters, fields=["name", party_group])
	party_names = [d.get("name") for d in party_list]
	party_groups = {d.get("name"): d.get(party_group) for d in party_list}

	for d in party_names:
		party_details.setdefault(d, frappe._dict())

	party_details = get_party_details(party_type, party_names, party_details)

	# Add a row for each party address and contact, along with party details
	for party, details in iteritems(party_details):
		territory = sales_partner = license_type = license_number = None

		if party_type == "Customer":
			territory = frappe.db.get_value(party_type, party, "territory")
			sales_partner = frappe.db.get_value(party_type, party, "default_sales_partner")

		if party_type in ("Customer", "Supplier"):
			license_record = get_default_license(party_type, party)

			if frappe.db.exists("Compliance Info", license_record):
				license_type, license_number = frappe.db.get_value(
					"Compliance Info", license_record, ["license_type", "license_number"])

		# If no addresses and contacts exist, add a single row to display the party
		addresses = details.get("address", [])
		contacts = details.get("contact", [])
		max_length = max(len(addresses), len(contacts), 1)

		for idx in range(max_length):
			result = [party]
			result.append(party_groups.get(party))

			if party_type == "Customer":
				result.extend([territory, sales_partner])

			if party_type in ("Customer", "Supplier"):
				result.extend([license_type, license_number])

			address = addresses[idx] if idx < len(addresses) else add_blank_columns_for("Address")
			contact = contacts[idx] if idx < len(contacts) else add_blank_columns_for("Contact")

			result.extend(address)
			result.extend(contact)
			data.append(result)

	return data
