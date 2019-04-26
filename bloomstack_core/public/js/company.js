frappe.ui.form.on("Company", {
	refresh: (frm) => {
		frm.add_custom_button(__("License Info"), () => {
			frappe.set_route("List", "Compliance Info", { "entity": frm.doc.name })
		}, __("View"))
	}
})