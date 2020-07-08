frappe.ui.form.on("Stock Entry Detail", {
	s_warehouse: function(frm, cdt, cdn){
		var row = locals[cdt][cdn];

		frappe.db.get_value("Warehouse", {"name" : row.s_warehouse}, ["customer", "supplier"], (r) => {
			if(r){
				frappe.model.set_value(cdt, cdn, "customer", r.customer);
				frappe.model.set_value(cdt, cdn, "supplier", r.supplier);
				refresh_field("items");
			}
		})
	},

	t_warehouse: function(frm, cdt, cdn){
		var row = locals[cdt][cdn];

		frappe.db.get_value("Warehouse", {"name" : row.t_warehouse}, ["customer", "supplier"], (r) => {
			if(r){
				frappe.model.set_value(cdt, cdn, "customer", r.customer);
				frappe.model.set_value(cdt, cdn, "supplier", r.supplier);
				refresh_field("items");
			}
		})
	}
})