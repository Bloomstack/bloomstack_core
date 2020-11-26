// Copyright (c) 2020, Bloom Stack, Inc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cubejs", {
	after_save: function(frm) {
		frappe.call({
			method:
				"bloomstack_core.bloomstack_core.page.admin_insights.admin_insights.get_cubejs_host",
			callback: (r) => {
				const dataUrl = `${r.message.cube_js_host}/api/restart`;
				$.ajax({
					url: dataUrl,
					cache: false,
					success: function (html) {
						alert("Server restarted successfully....");
					}
				});
			},
		});

	}
});
