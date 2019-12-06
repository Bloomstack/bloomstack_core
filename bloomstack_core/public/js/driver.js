// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Driver', {
	setup: function(frm) {
		frm.set_query('transporter', function(){
			return {
				filters: {
					'is_transporter': 1
				}
			};
		});
	},
	
	user_id: function(frm) {
		if(frm.doc.user_id) {
			frappe.db.get_value("Employee", {"user_id": frm.doc.user_id}, "name", (r) => {
				if(r && r.name) {
					frm.set_value("employee", r.name);
				}	
			});
		}
	},

	validate: function(frm) {
		if(!frm.doc.user_id) {
			frappe.msgprint(__("The driver will not be able to log in without a User ID"));
		}
	}
});
