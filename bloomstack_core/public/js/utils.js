$(document).on('app_ready', function() {
	$.each(["Purchase Invoice", "Purchase Receipt", "Purchase Order"], function(i, doctype) {
		frappe.ui.form.on(doctype, {
			supplier: (frm) => {
				if (frm.doc.supplier) {
					frappe.call({
						method: "bloomstack_core.hook_events.utils.validate_entity_license",
						args: {
							'entity': frm.doc.supplier
						}
					});
				}
			}
		});
	});

	$.each(["Quotation", "Sales Order", "Sales Invoice", "Delivery Note"], function (i, doctype) {
		frappe.ui.form.on(doctype, {
			customer: (frm) => {
				if (frm.doc.customer) {
					frappe.call({
						method: "bloomstack_core.hook_events.utils.validate_entity_license",
						args: {
							'entity': frm.doc.customer
						}
					})
				}
			}
		});
	});
});
