/* global frappe, erpnext, _ */

frappe.ui.form.on('Purchase Receipt Item', {
	batch_no: (frm, cdt, cdn) => {
		const row = frm.selected_doc;

		// set package tag from the selected batch, even if empty
		if (row.batch_no) {
			frappe.db.get_value("Batch", row.batch_no, "package_tag", (r) => {
				frappe.model.set_value(cdt, cdn, "package_tag", r.package_tag);
			})
		}

		// toggle read-only on package tag field if batch is selected
		let grid_row = frm.open_grid_row() || frm.get_field(row.parentfield).grid.get_row(cdn);
		if (grid_row) {
			grid_row.toggle_editable("package_tag", !row.batch_no);
		}
	}
});