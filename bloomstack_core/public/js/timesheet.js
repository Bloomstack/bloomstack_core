frappe.ui.form.on("Timesheet Detail", {
	project: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.project && row.billable === 0) {
			frappe.db.get_value("Project", { "name": row.project }, "billable", (r) => {
				if (r && r.billable === 1) {
					frappe.model.set_value(cdt, cdn, "billable", r.billable);
				}
			});
		}
	},

	task: function (frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.task && row.billable === 0) {
			frappe.db.get_value("Task", { "name": row.task }, "billable", (r) => {
				if (r && r.billable === 1) {
					frappe.model.set_value(cdt, cdn, "billable", r.billable);
				}
			});
		}
	},
});
