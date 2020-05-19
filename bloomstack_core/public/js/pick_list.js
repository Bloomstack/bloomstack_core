frappe.ui.form.on('Pick List Item', {
	package_tag: function (frm, cdt, cdn) {
		const row = frm.selected_doc || locals[cdt][cdn];

		if (row.package_tag) {
			frappe.db.get_value("Batch", {"package_tag": row.package_tag}, "name", (r) => {
				if (r && r.name) {
					if (row.batch_no) {
						// check if a different batch already exists, and ask for confirmation before overriding
						if (row.batch_no != r.name) {
							frappe.confirm(__("The {0} tag is linked to a different batch ({1}). Setting this package tag will not override the batch.<br><br>Do you still want to continue?", [row.package_tag, r.name]),
								() => {},
								() => {
									frappe.model.set_value(cdt, cdn, "package_tag", "");
								}
							);
						}
					} else {
						frappe.model.set_value(cdt, cdn, "batch_no", r.name);
					}
				}
			});
		}
	}
});
