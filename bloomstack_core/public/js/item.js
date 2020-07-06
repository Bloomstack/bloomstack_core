/* global frappe, erpnext, _ */

frappe.ui.form.on('Item', {
	refresh: (frm) => {
		if (frappe.boot.compliance_enabled && !frm.is_new()) {
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
		frm.set_value("is_sales_item", 0);
	},

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