frappe.ui.form.on("Customer", {
	refresh: (frm) => {
		if (!frm.is_new()) {
			frm.add_custom_button(__("License Info"), () => {
				frappe.set_route("List", "Compliance Info", { "entity": frm.doc.name })
			})
		}
	}
})