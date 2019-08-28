/* global frappe, erpnext, __ */

frappe.ui.form.on('Batch', {
	refresh: (frm) => {
		if (frm.doc.batch_qty > 0 && frm.doc.expiry_date <= frappe.datetime.now_date()) {
			frm.add_custom_button(__("Move to Waste"), () => {
				frappe.prompt({
					label: "Target Warehouse",
					fieldname: "warehouse",
					fieldtype: "Link",
					options: "Warehouse",
					reqd: 1
				},
				function (data) {
					frappe.model.open_mapped_doc({
						method: "bloomstack_core.utils.move_expired_batches",
						frm: frm,
						args: {
							warehouse: data.warehouse
						}
					});
				}, __("Select Warehouse"), __("Move"));
			});
		}
	}
});
