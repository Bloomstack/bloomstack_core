// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Driver', {
	user_id: function(frm) {
		if(frm.doc.user_id) {
			frappe.db.get_value("Employee", {"user_id": frm.doc.user_id}, "name", (r) => {
				if(r && r.name) {
					frm.set_value("employee", r.name);
				}	
			});
		}
	}
});
