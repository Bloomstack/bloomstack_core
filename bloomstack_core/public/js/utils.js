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

	$.each(["Sales Invoice Item", "Delivery Note Item", "Stock Entry Detail"], function (i, doctype) {
		frappe.ui.form.on(doctype, {
			package_tag: (frm, cdt, cdn) => {
				const row = frm.selected_doc;

				// set batch no from the selected package tag, even if none found
				if (row.package_tag) {
					frappe.db.get_value("Package Tag", row.package_tag, "batch_no", (r) => {
						frappe.model.set_value(cdt, cdn, "batch_no", r.batch_no);
					})
				}
			}
		});
	});

	$.each(["Project", "Task", "Project Template", "Project Type"], function (i, doctype) {
		frappe.ui.form.on(doctype, {
			billable: (frm) => {
				let confirm_message = ""
				frappe.call({
					method: "bloomstack_core.hook_events.utils.get_linked_documents",
					args: {
						doctype: frm.doc.doctype,
						name: frm.doc.name
					},
					freeze:true,
					callback: (r) => {
						if (!r.exc && r.message.count > 0) {
							// add confirmation message for cancelling all linked docs
							let links_text = "";
							let links = r.message.docs;
							const doctypes = Array.from(new Set(links.map(link => link.doctype)));

							for (let doctype of doctypes) {
								let docnames = links
									.filter((link) => link.doctype == doctype)
									.map((link) => frappe.utils.get_form_link(link.doctype, link.name, true))
									.join(", ");
								links_text += `<li><strong>${doctype}</strong>: ${docnames}</li>`

							}
							links_text = "<ul>" + links_text + "</ul>"

							confirm_message = `This <strong>${frm.doc.doctype}</strong> ${frm.doc.name} is linked with the following documents: ${links_text}`
							frappe.confirm(__(`${confirm_message} Do you want to set them as {0} too?`, [frm.doc.billable ? "billed" : "unbilled"]),
								() => {
									frappe.call({
										method: "bloomstack_core.hook_events.utils.update_timesheet_logs",
										args: {
											ref_dt: frm.doctype,
											ref_dn: frm.doc.name,
											billable: frm.doc.billable
										},
										callback: (r) => {
											frm.save();
										}
									})
								},
								() => {
									frm.doc.billable = !frm.doc.billable;
									refresh_field("billable");
									}
							);
						}
					}
				});
			}
		});
	});
});
