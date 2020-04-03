frappe.ui.form.on("Lead", {
	setup: (frm) => {
        frm.set_query("region", { "is_group": 1 });
    },
    onload: function(frm) {
		frm.set_query("territory", () => {
			if (frm.doc.region) {
				return {
					query: "bloomstack_core.services.lead.filter_territory",
					filters: {
						region: frm.doc.region
					}
				}
			}
		});

	},
});
