frappe.ui.form.on('Delivery Trip', {
	refresh: (frm) => {
		if (frm.doc.docstatus == 1 && frm.doc.status != "Completed") {
			if (frm.doc.status == "Scheduled") {
				frm.trigger("start");
			}
			else if (frm.doc.status == "In Transit") {
				frm.trigger("pause");
			}
			else if (frm.doc.status == "Paused") {
				frm.trigger("continue");
			}
			frm.trigger("end");
		}

		frappe.db.get_value("Google Maps Settings", { name: "Google Maps Settings" }, "enabled", (r) => {
			if (r.enabled == 0) {
				// Hide entire Map section if Google Maps is disabled
				let wrapper = frm.fields_dict.sb_map.wrapper
				wrapper.hide()
			} else {
				// Inject Google Maps data into map embed field
				let wrapper = frm.fields_dict.map_html.$wrapper;
				wrapper.html(frm.doc.map_embed);
			}
		});

		// Print delivery manifests
		if (frm.doc.docstatus === 1) {
			if (frm.doc.delivery_stops.length > 0) {
				let deliveryNotes = frm.doc.delivery_stops.map(stop => stop.delivery_note);
				deliveryNotes = [...new Set(deliveryNotes)];
				deliveryNotes = deliveryNotes.filter(Boolean);

				frm.add_custom_button(__("Print Shipping Manifests"), () => {
					if (deliveryNotes.length == 0) {
						frappe.msgprint(__("There are no Delivery Notes linked to any stop(s)"))
					} else {
						const w = window.open('/api/method/frappe.utils.print_format.download_multi_pdf?' +
							'doctype=' + encodeURIComponent("Delivery Note") +
							'&name=' + encodeURIComponent(JSON.stringify(deliveryNotes)) +
							'&format=' + encodeURIComponent(frm.doc.shipping_manifest_template || ""));

						if (!w) {
							frappe.msgprint(__('Please enable pop-ups'));
							return;
						}
					}
				}).addClass("btn-primary");
			};
		}
	},

	force_save_or_update: function (frm, cdt, cdn) {
		// `model.set_value` doesn't trigger a form change, so
		// force-dirty to allow the form to be saved or updated
		frm.dirty();
		frm.save_or_update();
	},

	start: (frm) => {
		frm.add_custom_button(__("Start"), () => {
			frappe.confirm(__("Are you sure you want to start the trip?"),
				() => {
					frappe.prompt({
						"label": "Odometer Start Value",
						"fieldtype": "Int",
						"fieldname": "odometer_start_value",
						"reqd": 1
					},
						(data) => {
							frappe.call({
								method: "bloomstack_core.hook_events.delivery_trip.create_or_update_timesheet",
								args: {
									"dt": frm.docname,
									"action": "start",
									"odometer_value": data.odometer_start_value,
								},
								callback: (r) => {
									frm.reload_doc();
								}
							})
						},
						__("Enter Odometer Value"));
				},
				() => {
					frm.reload_doc();
				}
			);
		}).addClass("btn-primary");
	},

	pause: (frm) => {
		frm.add_custom_button(__("Pause"), () => {
			frappe.confirm(__("Are you sure you want to pause the trip?"),
				() => {
					frappe.call({
						method: "bloomstack_core.hook_events.delivery_trip.create_or_update_timesheet",
						args: {
							"dt": frm.docname,
							"action": "pause"
						},
						callback: (r) => {
							frm.reload_doc();
						}
					})
				},
				() => {
					frm.reload_doc();
				}
			);

		}).addClass("btn-primary");
	},

	continue: (frm) => {
		frm.add_custom_button(__("Continue"), () => {
			frappe.confirm(__("Are you sure you want to continue the trip?"),
				() => {
					frappe.call({
						method: "bloomstack_core.hook_events.delivery_trip.create_or_update_timesheet",
						args: {
							"dt": frm.docname,
							"action": "continue"
						},
						callback: (r) => {
							frm.reload_doc();
						}
					})
				},
				() => {
					frm.reload_doc();
				}
			);

		}).addClass("btn-primary");
	},

	end: (frm) => {
		frm.add_custom_button(__("End"), () => {
			frappe.confirm(__("You're about to end the trip. Continue?"),
				() => {
					frappe.prompt({
						"label": "Odometer End Value",
						"fieldtype": "Int",
						"fieldname": "odometer_end_value",
						"reqd": 1,
						"default": frm.doc.odometer_start_value
					},
						(data) => {
							frappe.call({
								method: "bloomstack_core.hook_events.delivery_trip.create_or_update_timesheet",
								args: {
									"dt": frm.docname,
									"action": "end",
									"odometer_value": data.odometer_end_value,
								},
								callback: (r) => {
									frm.reload_doc();
								}
							})
						},
						__("Enter Odometer Value"));
				},
				() => {
					frm.reload_doc();
				}
			);

		}).addClass("btn-primary");
	},

});

frappe.ui.form.on("Delivery Stop", {
	visited: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];

		if (row.visited && row.sales_invoice) {
			if (row.paid_amount !== row.grand_total) {
				frappe.call({
					method: "bloomstack_core.hook_events.delivery_trip.update_payment_due_date",
					args: {
						sales_invoice: row.sales_invoice
					}
				})
			}
		}
	},

	make_payment_entry: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];

		let dialog = frappe.prompt({
			"label": "Payment Amount",
			"fieldtype": "Currency",
			"fieldname": "payment_amount",
			"reqd": 1
		},
		function (data) {
			if (data.payment_amount === 0) {
				frappe.confirm(
					__("Are you sure you want to complete this delivery without a payment?"),
					() => {
						frappe.model.set_value(cdt, cdn, "visited", true);
						frappe.model.set_value(cdt, cdn, "paid_amount", 0);
						frm.trigger("force_save_or_update");
					}
				);
			} else {
				frappe.call({
					method: "bloomstack_core.hook_events.delivery_trip.make_payment_entry",
					args: {
						"payment_amount": data.payment_amount,
						"sales_invoice": row.sales_invoice,
						"delivery_trip": frm.doc.name
					},
					callback: function (r) {
						if (!r.exc) {
							frappe.msgprint(__(`Payment Entry ${r.message} created.`));
							frappe.model.set_value(cdt, cdn, "visited", true);
							frappe.model.set_value(cdt, cdn, "paid_amount", data.payment_amount);
							frm.trigger("force_save_or_update");
						}
					}
				})
			}
		},
		__("Make Payment Entry"));

		dialog.$wrapper.on("shown.bs.modal", function() {
			if (frappe.is_mobile()) {
				dialog.$wrapper.find($('input[data-fieldtype="Currency"]')).attr('type', 'number');
			}
		});
	}
});