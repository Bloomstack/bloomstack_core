// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["Contract"] = {
	field_map: {
        "start": "end_date",
		"end": "end_date",
		"title": "name"
	},
	get_events_method: "frappe.desk.calendar.get_events"
}