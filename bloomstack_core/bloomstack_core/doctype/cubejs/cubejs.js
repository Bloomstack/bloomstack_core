// Copyright (c) 2020, Bloom Stack, Inc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cubejs', {
	after_save: function(frm) {
		frappe.call({
			method:
				"bloomstack_core.bloomstack_core.page.admin_insights.admin_insights.get_cubejs_host",
			callback: (r) => {
				console.log(r);
				const dataUrl = `${r.message.cube_js_host}/api/restart`
				$.ajax({
					url: dataUrl,
					cache: false,
					success: function (html) {
						alert("Server restarted successfully....");
					}
				});
			},
		});
		// const myWindow=window.open("http://localhost:4000/api/restart","__blank");
		// myWindow.close();
		// window.location.href = "http://localhost:4000/api/restart";
		// axios.post("http://localhost:4000/api/restart");
		// const url = "http://localhost:4000/api/restart";
		// const wp = "left=40, top=40, width=550, height=400, location=no, menubar=no, resizable=no, status=yes, toolbar=no";
		// window.open(url, "winnote", wp);
	}
});
