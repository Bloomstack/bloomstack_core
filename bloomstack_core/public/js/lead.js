frappe.ui.form.on("Lead", {
	setup: (frm) => {
		frm.set_query("region", { "is_group": 1 });
	},

	onload: (frm) => {
		frm.set_query("territory", () => {
			if (frm.doc.region) {
				return {
					query: "erpnext.crm.doctype.lead.lead.filter_territory",
					filters: {
						region: frm.doc.region
					}
				};
			}
		});

		if (!frm.doc.account_opened_date) {
			frappe.db.get_value("Customer", { "lead_name": frm.doc.name }, ["opening_date", "creation"], (r) => {
				if (r) {
					if (r.opening_date) {
						frm.set_value("account_opened_date", r.opening_date);
					} else {
						frm.set_value("account_opened_date", r.creation);
					}
				}
			});
		}
	}
});