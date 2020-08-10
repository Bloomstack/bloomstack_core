frappe.provide("bloomstack_core.utils");
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
				bloomstack_core.utils.set_and_update_excise_tax(frm);
			},
			order_type: (frm) => {
				if (frm.doc.order_type) {
					bloomstack_core.utils.set_and_update_excise_tax(frm);
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
				bloomstack_core.utils.set_and_update_excise_tax(frm);
			},

			item_code: (frm, cdt, cdn) => {
				if (frm.doc.total) {
					// update excise tax on item_code change.
					bloomstack_core.utils.set_and_update_excise_tax(frm);
				}
			},

			rate: (frm, cdt, cdn) => {
				// update excise tax on rate change.
				bloomstack_core.utils.set_and_update_excise_tax(frm);
			},

			items_remove: (frm, cdt, cdn) => {
				// update excise tax on items_remove
				bloomstack_core.utils.set_and_update_excise_tax(frm);
			}
		});
	});

	$.each(["Purchase Order", "Purchase Invoice"], function(i, doctype) {
		frappe.ui.form.on(doctype, {
			reverse_calculate: function(frm) {
				let data = [];
				for (let row of frm.doc.items) {
					data.push({
						"doctype": row.doctype,
						"docname": row.name,
						"item_code": row.item_code,
						"item_name": row.item_name,
						"qty": row.qty,
						"rate": row.rate,
						"amount": row.amount,
						"flower_weight": row.flower_weight,
						"leaf_weight": row.leaf_weight,
						"plant_weight": row.plant_weight,
						"uom": row.uom,
						"cultivation_weight_uom": row.cultivation_weight_uom
					})
				}

				const dialog = new frappe.ui.Dialog({
					title: __("Set Amount for Items"),
					fields: [
						{
							label: __("Items"),
							fieldname: "items",
							fieldtype: "Table",
							cannot_add_rows: true,
							data: data,
							in_place_edit: true,
							get_data: () => {
								return this.data;
							},
							fields: [
								{
									fieldtype: 'Data',
									fieldname: "docname",
									hidden: 1
								},
								{
									label: __("Item Code"),
									fieldtype: 'Link',
									fieldname: "item_code",
									options: "Item",
									read_only: 1,
									in_list_view: 1
								},
								{
									label: __("Item Name"),
									fieldtype: 'Data',
									fieldname: "item_name",
									read_only: 1,
									in_list_view: 1
								},
								{
									label: __("Qty"),
									fieldtype: 'Data',
									fieldname: 'qty',
									read_only: 1,
									in_list_view: 1
								},
								{
									label: __("Rate"),
									fieldtype: 'Data',
									fieldname: 'rate',
									read_only: 1,
									in_list_view: 1
								},
								{
									label: __("Amount"),
									fieldtype: 'Data',
									fieldname: 'amount',
									in_list_view: 1
								}
							],
						}
					],
					primary_action: function () {
						const values = dialog.get_values().items;
						frappe.call({
							method: "bloomstack_core.hook_events.taxes.get_cultivation_tax",
							freeze: true,
							args: {
								"doc": frm.doc,
								"items": values
							},
							callback: function(r) {
								let items = r.message;
								items.forEach(item => {
									let rate = item.amount / item.qty;
									frappe.model.set_value(item.doctype, item.docname, "rate", rate);
								});
							}
						})
						dialog.hide();
						frappe.show_alert({
							indicator: 'green',
							message: __("The amounts have been successfully set")
						});
					},
					primary_action_label: __('Set Amounts')
				})
				dialog.show();
			}
		})
	})
});

$.extend(bloomstack_core.utils, {
	set_and_update_excise_tax: function(frm) {
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
									frm.add_child('taxes', excise_tax_row);
									frm.refresh_field('taxes');
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
});
