
frappe.provide('bloomstack_core');

// add toolbar icon
$(document).bind('toolbar_setup', function() {
	frappe.app.name = "Bloomstack";

	var $logo = $('<img class="erpnext-icon"/>')
		.attr('src', '/assets/bloomstack_core/images/icon.png');

	$('.navbar-home').empty().append($logo);
});
