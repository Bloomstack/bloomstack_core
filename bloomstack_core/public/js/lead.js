frappe.ui.form.on("Lead", {
    setup: (frm) => {
        frm.set_query("region", { "is_group": 1 });
    },

    onload: (frm) => {
        frm.set_query("territory", () => {
            if (frm.doc.region) {
                return {
                    query: "bloomstack_core.hook_events.lead.filter_territory",
                    filters: {
                        region: frm.doc.region
                    }
                };
            }
        });

        if (frm.doc.status == 'Converted') {
            frappe.db.get_value("Customer", { "lead_name": frm.doc.name }, "creation", (r) => {
                if (r) {
                    frm.set_value("account_opened_date", r.creation);
                }
            });
        }
    }
});