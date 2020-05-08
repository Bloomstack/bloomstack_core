$(document).ready(function () {
	$(document).on('click', '.address-box a.unlink_address', function() {
		var name = $(this).attr('address_name');
		unlink_address(name);
	});

	function unlink_address(name) {
		frappe.confirm(
			'Are you sure to unlink this address?',
			function(){
				frappe.model.with_doc("Address", name, ()=> {
					address = frappe.model.get_doc("Address", name);
					frappe.call({
						method: "bloomstack_core.utils.unlink_address",
						args: {"doc": address, "doctype": cur_frm.doctype, "name": cur_frm.docname },
						callback: function () {
							window.location.reload()
						}
					})
					// console.log(address2);
				})
			},
			function(){
				window.close();
			}
	);
	}

	$(document).on('click', '.address-box a.delete_address', function() {
		var name = $(this).attr('address_name');
		delete_address(name);
	});

	function delete_address(name) {
		frappe.confirm(
			'Are you sure to delete this address?',
			function(){
				frappe.model.with_doc("Address", name, ()=> {
					address = frappe.model.get_doc("Address", name);
					frappe.call({
						method: "bloomstack_core.utils.delete_address",
						args: {"doc": address, "doctype": cur_frm.doctype, "name": cur_frm.docname },
						callback: function () {
							window.location.reload()
						}
					})
				})
			},
			function(){
				window.close();
			}
	);
	}

	
});

