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
							if (r.message) {
								frm.set_value("license", r.message);
							}
						}
					});
				}
			}
		});
	});

	$.each(["Quotation", "Sales Order", "Sales Invoice", "Delivery Note"], function (i, doctype) {
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
							if (r.message) {
								frm.set_value("license", r.message);
								frappe.show_alert({
									indicator: 'blue',
									message: __(`The following license was set for ${frm.doc.customer}: ${r.message.bold()}`)
								});
							}
						}
					});
				}

				// set excise tax if customer has license number
				set_and_update_excise_tax(frm);
			},
			order_type: (frm) => {
				if (frm.doc.order_type) {
					set_and_update_excise_tax(frm);
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

	$.each(["Sales Order Item", "Sales Invoice Item", "Delivery Note Item", "Stock Entry Detail"], function (i, doctype) {
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

	$.each(["Quotation Item", "Sales Invoice Item", "Delivery Note Item", "Sales Order Item"], function (i, doctype) {
		frappe.ui.form.on(doctype, {
			qty: (frm, cdt, cdn) => {
				// update excise tax on qty change.
				set_and_update_excise_tax(frm);
			},

			item_code: (frm, cdt, cdn) => {
				if (frm.doc.total) {
					// update excise tax on item_code change.
					set_and_update_excise_tax(frm);
				}
			},

			rate: (frm, cdt, cdn) => {
				// update excise tax on rate change.
				set_and_update_excise_tax(frm);
			},

			items_remove: (frm, cdt, cdn) => {
				// update excise tax on items_remove
				set_and_update_excise_tax(frm);
			}
		});
	});

	$.each(["Project", "Task", "Project Template", "Project Type"], function (i, doctype) {
		frappe.ui.form.on(doctype, {
			billable: (frm) => {
				let confirm_message = "";
				frappe.call({
					method: "bloomstack_core.hook_events.utils.get_linked_documents",
					args: {
						doctype: frm.doc.doctype,
						name: frm.doc.name
					},
					freeze: true,
					callback: (r) => {
						if (!r.exc && r.message.count > 0) {
							// add confirmation message for cancelling all linked docs
							let links_text = "";
							let links = r.message.docs;
							const doctypes = Array.from(new Set(links.map((link) => link.doctype)));

							for (let doctype of doctypes) {
								let docnames = links
									.filter((link) => link.doctype === doctype)
									.map((link) => frappe.utils.get_form_link(link.doctype, link.name, true))
									.join(", ");
								links_text += `<li><strong>${doctype}</strong>: ${docnames}</li>`;

							}
							links_text = "<ul>" + links_text + "</ul>";

							confirm_message = `${frm.doc.name.bold()} is linked with the following documents: ${links_text}`;
							frappe.confirm(__(`${confirm_message} Do you want to set them as <strong>{0}</strong> too?`, [frm.doc.billable ? "billable" : "non-billable"]),
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

set_and_update_excise_tax = function(frm) {
	cur_frm.cscript.calculate_taxes_and_totals();
	if (frm.doc.license) {
		frappe.db.get_value("Compliance Info", { "name": frm.doc.license }, "license_for", (r) => {
			if (r && r.license_for == "Retailer") {
				frappe.call({
					method: "bloomstack_core.hook_events.taxes.set_excise_tax",
					args: {
						doc: frm.doc
					},
					callback: (r) => {
						console.log("r.message", r.message);
						if (r.message && r.message.tax_amount > 0) {
							let excise_tax_row = r.message;
							let taxes = frm.doc.taxes;

							if (taxes && taxes.length > 0) {
								$.each(taxes, function (i, tax) {
									if (tax.account_head == excise_tax_row.account_head) {
										tax.tax_amount = excise_tax_row.tax_amount
									} else {
										frm.add_child('taxes', excise_tax_row);
									}
								});
							} else {
								console.log("else", excise_tax_row);
								frm.add_child('taxes', excise_tax_row);
								frm.refresh_field('taxes')
								cur_frm.cscript.calculate_taxes_and_totals();
							}
						} else if ((r.message && r.message.tax_amount == 0)) {
							let taxes = frm.doc.taxes;
							if (taxes && taxes.length > 0) {
								$.each(taxes, function (i, tax) {
									if (tax.account_head == r.message.account_head) {
										frm.get_field("taxes").grid.grid_rows[i].remove();
									}
								});
							}
						}
					}
				})
			};
		})
	}
}
