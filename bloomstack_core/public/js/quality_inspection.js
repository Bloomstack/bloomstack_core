/* global frappe, erpnext, _ */

frappe.ui.form.on('Quality Inspection', {
	package_tag: (frm) => {
		// set package tag from the selected batch, even if empty
		if (frm.doc.package_tag) {
			frappe.db.get_value("Package Tag", frm.doc.package_tag, "batch_no", (r) => {
				frm.set_value("batch_no", r.batch_no);
			});
		}
	}
});