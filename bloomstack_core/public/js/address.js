$(document).ready(function () {

	$(document).on('click', '.address-box a.unlink_address', function () {
		var name = $(this).attr('data_address_name');
		frappe.confirm(
			'Are you sure you want to unlink this address linked with '+cur_frm.docname+'?',
			function () {
				frappe.call({
					method: "bloomstack_core.utils.unlink_address",
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

	$(document).on('click', '.address-box a.delete_address', function () {
		var name = $(this).attr('data_address_name');
		frappe.confirm(
			'If this address is linked to any other user in the system, it will just remove the address from '+cur_frm.docname+'.<br> Are you sure you want to delete this address linked with '+cur_frm.docname+'?',
			function () {
				frappe.call({
					method: "bloomstack_core.utils.delete_address",
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