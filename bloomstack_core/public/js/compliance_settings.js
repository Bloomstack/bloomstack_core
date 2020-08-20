frappe.ui.form.on("Compliance Settings", {
	refresh: (frm) => {
		frm.add_custom_button(__("Sync Data"), () => {
			frappe.call({
				method: "bloomstack_core.compliance.settings.sync_data"
			});
		}).addClass("btn-primary");
	}
});