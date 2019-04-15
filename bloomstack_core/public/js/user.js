frappe.ui.form.on("User", {
	refresh: (frm) => {
		bloomstack_core.add_login_as_button(frm,
			__("Login As ") + frm.doc.first_name + (frm.doc.last_name ? " " + frm.doc.last_name : ""),
			frm.doc.name);
	}
});