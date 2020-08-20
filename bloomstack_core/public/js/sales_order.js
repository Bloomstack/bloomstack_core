/* global frappe, erpnext, _ */

frappe.ui.form.on('Sales Order', {
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
	}
});
