frappe.ui.form.on('Delivery Note', {
	refresh: (frm) => {
		if (frm.doc.is_return) {
			// Default all returns to be issued with credit notes
			frm.doc.issue_credit_note = 1;

			// Change label for warehouse fields in case of returns
			frm.set_df_property("set_warehouse", "label", "Set Return Warehouse");
			frm.toggle_display("to_warehouse");
		}
	}
});