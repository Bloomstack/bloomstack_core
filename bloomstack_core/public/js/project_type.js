frappe.ui.form.on("Project Type", {
	billable: (frm) => {
		frappe.confirm(__(`Do you want to update linked timesheets with billable status as ${frm.doc.billable} ?`),
			() => {
				frappe.call({
					method: "bloomstack_core.hook_events.utils.update_timesheet_logs",
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