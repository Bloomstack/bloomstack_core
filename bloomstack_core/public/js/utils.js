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
								frappe.show_alert({
									indicator: 'blue',
									message: __(r.message + "license set for customer")
								});
							}
						}
					})
				}
				if (frm.doc.license) {
					frappe.call({
						method: "bloomstack_core.hook_events.taxes.set_excise_tax",
						args: {
							doc: frm.doc
						},
						callback: (r) => {
							if(r.message){
								let taxes = frm.doc.taxes;
								if (taxes && taxes.length > 0){
									$.each(taxes, function (i, d) {
										if (d.account_head == r.message.account_head ) {
											d.tax_amount = r.message.tax_amount
										} 
										else 
										{
											frm.add_child('taxes',  r.message);
										}
									});
								}
								else {
									frm.add_child('taxes',  r.message);
								}
							}
						}
					})
				}
			}
		});
	});

	$.each(["Customer", "Supplier", "Company"], function (i, doctype) {
		frappe.ui.form.on(doctype, {
			refresh: (frm) => {
				frm.set_query("license", "licenses", (doc, cdt, cdn) => {
					const set_licenses = doc.licenses.map(license => license.license);
					return {
						query: "bloomstack_core.utils.get_active_licenses",
						filters: {
							set_licenses: set_licenses
						}
					}
				});
			}											
		});																																
	});
});
