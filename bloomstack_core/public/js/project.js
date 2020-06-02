frappe.ui.form.on("Project", {
	project_template: (frm) => {
		if (frm.is_new() && frm.doc.project_template) {
			if (frm.doc.billable === 0) {
				frappe.db.get_value("Project Template", { "name": frm.doc.project_template }, "billable", (r) => {
					if (r && r.billable === 1) {
						frm.set_value("billable", 1);
					}
				});
			}
		}
	},

	project_type: (frm) => {
		if (frm.doc.billable === 0) {
			frappe.db.get_value("Project Type", { "name": frm.doc.project_type }, "billable", (r) => {
				if (r && r.billable === 1) {
					frm.set_value("billable", 1)
				}
			});
		}
	}
});