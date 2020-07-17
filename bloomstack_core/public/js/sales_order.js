/* global frappe, erpnext, _ */

frappe.ui.form.on('Sales Order', {
	refresh: (frm,) => {
		frm.set_query("package_tag", "items", (doc, cdt, cdn) => {
			let row = frm.selected_doc || locals[cdt][cdn];

			if (!row.batch_no) {
				return { filters: { "item_code": row.item_code } };
			} else {
				return { filters: { "item_code": row.item_code, "batch_no": row.batch_no } };
			}
		})
	},

	no_charge_order: (frm) => {
		frm.trigger("set_promotional_discount");
	},

	set_promotional_discount: (frm) => {
		let percentage_discount = 0;

		if (frm.doc.no_charge_order) {
			frm.set_value("apply_discount_on", "Grand Total");
			percentage_discount = 100;
		}

		frm.set_value("additional_discount_percentage", percentage_discount);

		frappe.show_alert({
			indicator: 'green',
			message: __(`${percentage_discount}% discount applied`)
		});
	},

	delivery_date: function(frm) {
		$.each(frm.doc.items || [], function(i, d) {
			d.delivery_date = frm.doc.delivery_date;
		});
		refresh_field("items");
	}
});
