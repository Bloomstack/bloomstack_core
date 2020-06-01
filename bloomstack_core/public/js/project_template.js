frappe.ui.form.on("Project Template", {
	billable: (frm) => {
		frappe.confirm(__(`Do you want to update this template's linked projects and timesheets to be set as {0}?`, [frm.doc.billable ? "billed" : "unbilled"]),
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