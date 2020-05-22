// Copyright (c) 2020, Bloom Stack, Inc and contributors
// For license information, please see license.txt

frappe.ui.form.on('License', {
	refresh: (frm) => {
		if (!frm.is_new()) {
			if (!frm.doc.license_expiry_date || frm.doc.license_expiry_date > frappe.datetime.get_today()) {
				frm.add_custom_button(__("Customer"), () => {
					frappe.model.open_mapped_doc({
						method: "bloomstack_core.utils.create_customer",
						frm: frm
					});
				}, __("Create"));

				frm.add_custom_button(__("Supplier"), () => {
					frappe.model.open_mapped_doc({
						method: "bloomstack_core.utils.create_supplier",
						frm: frm
					});
				}, __("Create"));
			}
		}
	}
});
