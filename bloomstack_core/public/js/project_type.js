frappe.ui.form.on("Project Type", {
	billable: (frm) => {
		frappe.confirm(__(`Do you want to update this project type's linked projects and timesheets to be set as {0}?`, [frm.doc.billable ? "billed" : "unbilled"]),
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
				frm.set_value("billable", !frm.doc.billable);
			}
		);
	}
});