frappe.ui.form.on('Pick List Item', {
	package_tag: function (frm, cdt, cdn) {
		const row = frm.selected_doc || locals[cdt][cdn];

		if (row.package_tag) {
			frappe.db.get_value("Batch", {"package_tag": row.package_tag}, "name", (r) => {
				if (r && r.name) {
					// check if a different batch already exists
					if (row.batch_no && row.batch_no != r.name) {
						frappe.throw(__(`The "${row.package_tag}" tag is linked to a different batch (${r.name})`));
					} else {
						frappe.model.set_value(cdt, cdn, "batch_no", r.name);
					}
				}
			});
		}
	}
});
