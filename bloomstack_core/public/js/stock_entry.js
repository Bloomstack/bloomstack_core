frappe.ui.form.on("Stock Entry Detail", {
	s_warehouse: function (frm, cdt, cdn) {
		const row = locals[cdt][cdn];

		if (row.s_warehouse) {
			frappe.db.get_value("Warehouse", { "name": row.s_warehouse }, ["customer", "supplier"], (r) => {
				frappe.model.set_value(cdt, cdn, "customer", r.customer || row.customer);
				frappe.model.set_value(cdt, cdn, "supplier", r.supplier || row.supplier);
				refresh_field("items");
			})
		} else if (row.t_warehouse) {
			frm.script_manager.trigger('t_warehouse', cdt, cdn);
		} else {
			frappe.model.set_value(cdt, cdn, "customer", "");
			frappe.model.set_value(cdt, cdn, "supplier", "");
		}
	},

	t_warehouse: function (frm, cdt, cdn) {
		const row = locals[cdt][cdn];

		if (row.t_warehouse) {
			frappe.db.get_value("Warehouse", { "name": row.t_warehouse }, ["customer", "supplier"], (r) => {
				frappe.model.set_value(cdt, cdn, "customer", r.customer || row.customer);
				frappe.model.set_value(cdt, cdn, "supplier", r.supplier || row.supplier);
				refresh_field("items");
			})
		} else if (row.s_warehouse) {
			frm.script_manager.trigger("s_warehouse", cdt, cdn);
		} else {
			frappe.model.set_value(cdt, cdn, "customer", "");
			frappe.model.set_value(cdt, cdn, "supplier", "");
		}
	}
})