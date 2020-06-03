frappe.ui.form.on("Task", {
	project: (frm) => {
		if (frm.doc.project && frm.doc.billable === 0) {
			frappe.db.get_value("Project", { "name": frm.doc.project }, "billable", (r) => {
				if (r && r.billable === 1) {
					frm.set_value("billable", 1);
				}
			});
		}
	}
});
