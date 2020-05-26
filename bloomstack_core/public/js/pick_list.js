frappe.ui.form.on('Pick List', {
	setup: (frm) => {
		frm.set_query('package_tag', 'locations', (frm, cdt, cdn) => {
			const row = frm.selected_doc || locals[cdt][cdn];
			return {
				filters: {
					"item_code": ["IN", [row.item_code, ""]]
				}
			}
		})
	}
})

frappe.ui.form.on('Pick List Item', {
	package_tag: (frm, cdt, cdn) => {
		const row = frm.selected_doc || locals[cdt][cdn];

		if (row.package_tag) {
			frappe.db.get_value("Package Tag", {"name": row.package_tag}, "batch_no", (r) => {
				if (r && r.batch_no) {
					// check if a different batch already exists
					if (row.batch_no && row.batch_no != r.batch_no) {
						frappe.throw(__(`The "${row.package_tag}" tag is linked to a different batch (${r.batch_no})`));
					} else {
						frappe.model.set_value(cdt, cdn, "batch_no", r.batch_no);
					}
				}
			});
		}
	}
});