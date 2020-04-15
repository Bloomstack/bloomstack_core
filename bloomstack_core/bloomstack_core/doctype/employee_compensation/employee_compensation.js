// Copyright (c) 2020, Bloom Stack, Inc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Compensation', {
	validate: function(frm) {
		if (frm.doc.date_of_injury > frappe.datetime.get_today()) {
			frappe.msgprint(__("You can not select future date in Date of Injury"));
			frappe.validated = false;
		}
		if (frm.doc.first_aid_date > frappe.datetime.get_today()) {
			frappe.msgprint(__("You can not select future date in first Aid"));
			frappe.validated = false;
		}
		if (frm.doc.first_aid_date < frm.doc.date_of_injury) {
			frappe.msgprint(__("You can not select first aid date less than Injury Date"));
			frappe.validated = false;
		}
	}
});