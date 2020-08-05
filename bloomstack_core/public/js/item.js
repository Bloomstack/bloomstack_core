/* global frappe, erpnext, _ */

frappe.ui.form.on('Item', {
	item_name: (frm) => {
		if (frm.is_new()) {
			frm.trigger("build_item_code");
		}
	},

	item_group: (frm) => {
		if (frm.is_new()) {
			frm.trigger("build_item_code");
		}
	},

	brand: (frm) => {
		if (frm.is_new()) {
			frm.trigger("build_item_code");
		}
	},

	build_item_code: (frm) => {
		// TODO: allow toggling autoname from the website
		frappe.call({
			method: "bloomstack_core.hook_events.item.autoname_item",
			args: { item: frm.doc },
			callback: (r) => {
				if (r.message) {
					frm.set_value("item_code", r.message);
				}
			}
		})
	}
});