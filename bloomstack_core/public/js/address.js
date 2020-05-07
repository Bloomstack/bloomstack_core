$(document).ready(function () {
	$(document).on('click', '.address-box a.unlink_address', function() {
		frappe.confirm(
			'Are you sure to unlink this address?',
			function(){
					// yes
			},
			function(){
				window.close();
			}
	)	
	});

	$(document).on('click', '.address-box a.delete_address', function() {
		frappe.confirm(
			'Are you sure to delete this address?',
			function(){
					// yes
			},
			function(){
				window.close();
			}
	)	
	});

});