frappe.ui.form.on("Task", {
	project: (frm) => {
		frappe.db.get_value("Project", { "name": frm.doc.project }, "billable", (r) => {
			if (r && r.billable == 1) {
				frm.set_value("billable", 1)
			} else {
				frm.set_value("billable", 0)
			}
		});
	},
	billable: (frm) => {
		frappe.confirm(__(`Do you want to update linked timesheets with billable status as ${frm.doc.billable} ?`),
			() => {
				frappe.call({
					method: "bloomstack_core.hook_events.utils.update_timesheets",
					args: {
						ref_dt: frm.doctype,
						ref_dn: frm.doc.name,
						billable: frm.doc.billable
					}
				})
			},
			() => {}
		);
	}
});