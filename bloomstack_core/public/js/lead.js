frappe.ui.form.on("Lead", {
	setup: (frm) => {
        frm.set_query("region", { "is_group": 1 });
    },
    onload: function(frm) {
		frm.set_query('territory', function(doc) {
			return {
				filters: {
					"is_group": 0,
					"parent_territory": doc.region
				}
			};
		});
	},
});
