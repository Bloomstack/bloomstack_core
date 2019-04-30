/* global frappe, erpnext, _ */

frappe.ui.form.on('Item', {
	refresh: (frm) => {
		if (!frm.is_new()) {
			frappe.db.get_value("Compliance Item", { "item_code": frm.doc.item_code }, "name", (r) => {
				if (r && r.name) {
					frm.add_custom_button(__("View / Update"), () => {
						frappe.set_route("Form", "Compliance Item", r.name);
					}, __("Compliance"));
				};

				if (!r || !r.name) {
					frm.add_custom_button(__("Create"), () => {
						frm.make_new("Compliance Item");
					}, __("Compliance"));
				};
			})
		}
	}
});