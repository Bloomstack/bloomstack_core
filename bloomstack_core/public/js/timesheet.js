frappe.ui.form.on("Timesheet", {
	
});

frappe.ui.form.on("Timesheet Detail", {
	project: function(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		frappe.db.get_value("Project", { "name": row.project }, "billable", (r) => {
			if (r && r.billable == 1) {
				row.billable = 1
				refresh_field("billable", cdn, "time_logs");
			} else {
				row.billable = 0
				refresh_field("billable", cdn, "time_logs");
			}
		});
	},
	task: function(frm,cdt,cdn) {
		var row = locals[cdt][cdn];
		frappe.db.get_value("Task", { "name": row.task }, "billable", (r) => {
			if (r && r.billable == 1) {
				row.billable = 1
				refresh_field("billable", cdn, "time_logs");
			} else {
				row.billable = 0
				refresh_field("billable", cdn, "time_logs");
			}
		});
	},
});