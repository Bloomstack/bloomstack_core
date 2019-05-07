// Copyright (c) 2019, Bloom Stack, Inc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Compliance Settings', {
	is_metrc_enabled: (frm) => {
		frm.trigger("toggle_metrc_fields");
	},

	toggle_metrc_fields: (frm) => {
		frm.toggle_reqd(["metrc_url", "metrc_license_no", "metrc_vendor_key", "metrc_user_key"], frm.doc.is_metrc_enabled);
	}
});
