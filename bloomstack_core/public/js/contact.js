$(document).ready(function () {

	$(document).on('click', '.address-box a.unlink_contact', function () {
		var name = $(this).attr('data_contact_name');
		frappe.confirm(
			'Are you sure you want to unlink this contact linked with '+cur_frm.docname+'?',
			function () {
				frappe.call({
					method: "bloomstack_core.utils.unlink_contact",
					args: {
						"doc": name,
						"doctype": cur_frm.doctype,
						"name": cur_frm.docname
					},
					callback: function () {
						window.location.reload()
					}
				})
			}
		);
	});

	$(document).on('click', '.address-box a.delete_contact', function () {
		var name = $(this).attr('data_contact_name');
		frappe.confirm(
			'If this contact is associated to any other user in the system, it will just remove the contact from '+cur_frm.docname+'.<br> Are you sure you want to delete this contact linked with '+cur_frm.docname+'?',
			function () {
				frappe.call({
					method: "bloomstack_core.utils.delete_contact",
					args: {
						"doc": name,
						"doctype": cur_frm.doctype,
						"name": cur_frm.docname
					},
					callback: function () {
						window.location.reload()
					}
				})
			}
		);
	});

});