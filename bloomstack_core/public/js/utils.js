$(document).on('app_ready', function() {
	$.each(["Supplier Quotation", "Purchase Order", "Purchase Invoice", "Purchase Receipt"], function(i, doctype) {
		frappe.ui.form.on(doctype, {
			onload: (frm) => {
				frm.set_query("license", () => {
					return {
						query: "bloomstack_core.hook_events.utils.filter_license",
						filters: {
							party_name: frm.doc.supplier
						}
					};

				});
			},
			supplier: (frm) => {
				if (frm.doc.supplier) {
					frappe.call({
						method: "bloomstack_core.hook_events.utils.validate_entity_license",
						args: {
							party_type: "Supplier",
							party_name: frm.doc.supplier
						},
						callback: (r) => {
							if(r.message){
								frm.set_value("license", r.message)
							}
						}
					});
				}
			}
		});
	});

	$.each(["Sales Order", "Sales Invoice", "Delivery Note"], function (i, doctype) {
		frappe.ui.form.on(doctype, {
			onload: (frm) => {
				frm.set_query("license", () => {
					return {
						query: "bloomstack_core.hook_events.utils.filter_license",
						filters: {
							party_name: frm.doc.customer
						}
					};

				});
			},
			customer: (frm) => {
				if (frm.doc.customer) {
					frappe.call({
						method: "bloomstack_core.hook_events.utils.validate_entity_license",
						args: {
							party_type: "Customer",
							party_name: frm.doc.customer
						},
						callback: (r) => {
							if(r.message){
								frm.set_value("license", r.message)
							}
						}
					})
				}
			}
		});
	});
});
