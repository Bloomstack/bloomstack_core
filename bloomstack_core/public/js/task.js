frappe.ui.form.on("Task", {
	project: (frm) => {
		frappe.db.get_value("Project", { "name": frm.doc.project }, "billable", (r) => {
			if (r && r.billable == 1) {
				frm.set_value("billable", 1)
			}
		});
	},

	billable: (frm) => {
		frappe.confirm(__(`Do you want to update this task's linked timesheets to be set as {0}?`, [frm.doc.billable ? "billed" : "unbilled"]),
			() => {
				frappe.call({
					method: "bloomstack_core.hook_events.utils.update_timesheet_logs",
					args: {
						ref_dt: frm.doctype,
						ref_dn: frm.doc.name,
						billable: frm.doc.billable
					},
					callback: (r) => {
						frm.save();
					}
				})
			},
			() => {
				frm.reload_doc();
			}
		);
	}
});