/* global frappe, erpnext, _ */

frappe.ui.form.on('Item', {
	onload: (frm) => {
		frm.set_query("metrc_item_category", () => {
			if (frm.doc.metrc_uom) {
				return {
					query: "erpnext.stock.doctype.item.item.metrc_item_category_query",
					filters: {
						metrc_uom: frm.doc.metrc_uom
					}
				};
			}
		});

		frm.set_query("metrc_uom", () => {
			if (frm.doc.metrc_item_category) {
				return {
					query: "erpnext.stock.doctype.item.item.item.metrc_uom_query",
					filters: {
						metrc_item_category: frm.doc.metrc_item_category
					}
				};
			}
		});

		frm.set_query("metrc_unit_uom", () => {
			if (frm.doc.metrc_item_category) {
				return {
					query: "erpnext.stock.doctype.item.item.metrc_unit_uom_query",
					filters: {
						metrc_item_category: frm.doc.metrc_item_category
					}
				};
			}
		});
	},

	refresh: (frm) => {
		frm.trigger("toggle_metrc_fields_display");
	},

	metrc_uom: (frm) => {
		frm.trigger("toggle_metrc_fields_display");
	},

	toggle_metrc_fields_display: (frm) => {
		if (frm.doc.metrc_uom) {
			frappe.db.get_value("Compliance UOM", { "name": frm.doc.metrc_uom }, "quantity_type", (r) => {
				if (!r.exc) {
					frm.toggle_display("metrc_unit_value", r.quantity_type === "CountBased");
					frm.toggle_display("metrc_unit_uom", r.quantity_type === "CountBased");
				}
			});
		}
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
			method: "erpnext.stock.doctype.item.item.autoname_item",
			args: { item: frm.doc },
			callback: (r) => {
				if (r.message) {
					frm.set_value("item_code", r.message);
				}
			}
		})
	}
});