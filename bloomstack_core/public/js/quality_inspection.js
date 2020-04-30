/* global frappe, erpnext, _ */

frappe.ui.form.on('Quality Inspection', {
	batch_no: (frm) => {
		// set package tag from the selected batch, even if empty
		if (frm.doc.batch_no) {
			frappe.db.get_value("Batch", frm.doc.batch_no, "package_tag", (r) => {
				frm.set_value("package_tag", r.package_tag);
			})
		}

		// toggle read-only on package tag field if batch is selected
		frm.toggle_enable("package_tag", !frm.doc.batch_no);
	}
});