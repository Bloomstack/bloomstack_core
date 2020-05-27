frappe.ui.form.on("Task", {
	project: (frm) => {
		frappe.db.get_value("Project", { "name": frm.doc.project }, "billable", (r) => {
			if (r && r.billable == 1) {
				frm.set_value("billable", 1)
			} else {
				frm.set_value("billable", 0)
			}
		});
	}
});