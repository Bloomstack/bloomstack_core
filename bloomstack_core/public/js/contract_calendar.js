// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["Contract"] = {
	field_map: {
		"start": "start_date",
		"end": "end_date",
		"allDay": "allDay",
		"title": "name"
	},
	filters: [
		{
			"fieldtype": "select",
			"fieldname": "document_type",
			"label": __("Document")
		},
		{
			"fieldtype": "Link",
			"fieldname": "document_name",
			"options": "document_type",
			"label": __("Document")
		}
	],
	get_events_method: "bloomstack_core.hook_events.contract.get_events"
};