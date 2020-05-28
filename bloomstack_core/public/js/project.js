frappe.ui.form.on("Project", {
	project_template: (frm) => {
		if (frm.is_new && frm.doc.project_template) {
			frappe.db.get_value("Project Template", { "name": frm.doc.project_template }, "billable", (r) => {
				if (r && r.billable == 1) {
					frm.set_value("billable", 1)
				} else {
					frm.set_value("billable", 0)
				}
			});
		}
	},
	project_type: (frm) => {
		frappe.db.get_value("Project Type", { "name": frm.doc.project_type }, "billable", (r) => {
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
						doctype: frm.doctype,
						doc: frm.doc.name,
						billable: frm.doc.billable
					}
				})
			},
			() => {}
		);
	}
});