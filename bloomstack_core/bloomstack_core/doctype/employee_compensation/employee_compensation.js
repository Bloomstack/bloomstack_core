// Copyright (c) 2020, Bloom Stack, Inc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Compensation', {
	validate: function(frm) {
		if (frm.doc.date_of_injury > frappe.datetime.get_today()) {
			frappe.throw(__("You cannot select a future date for Date of Injury"));
		}
		if (frm.doc.first_aid_date > frappe.datetime.get_today()) {
			frappe.throw(__("You cannot select a future date for First Aid Date"));
		}
		if (frm.doc.first_aid_date < frm.doc.date_of_injury) {
			frappe.throw(__("The First Aid date cannot be before the Date of Injury"));
		}
	}
});