frappe.ui.form.on('Delivery Trip', {
	refresh: (frm) => {
		if (frm.doc.docstatus == 1 && frm.doc.status != "Completed") {
			if (frm.doc.odometer_start_value == 0) {
				frm.add_custom_button(__("Start"), () => {
					frappe.prompt({
						"label": "Odometer Start Value",
						"fieldtype": "Int",
						"fieldname": "odometer_start_value",
						"reqd": 1
					},
					(data) => {
						frm.set_value('odometer_start_value', data.odometer_start_value);
						frm.set_value('odometer_start_time', frappe.datetime.now_datetime());
						frm.dirty();
						frm.save_or_update();
					},
					__("Enter Odometer Value"));
				}).addClass("btn-primary");
			} else if (frm.doc.odometer_start_value > 0 && frm.doc.odometer_stop_value == 0) {
				frm.add_custom_button(__("Stop"), () => {
					frappe.prompt({
						"label": "Odometer Stop Value",
						"fieldtype": "Int",
						"fieldname": "odometer_stop_value",
						"reqd": 1
					},
					(data) => {
						if (data.odometer_stop_value > frm.doc.odometer_start_value) {
							frm.set_value('odometer_stop_value', data.odometer_stop_value);
							frm.set_value('odometer_stop_time', frappe.datetime.now_datetime());
							frm.set_value('actual_distance_travelled', (data.odometer_stop_value - frm.doc.odometer_start_value));
							frm.dirty();
							frm.save_or_update();
						} else {
							frappe.throw("The stop value cannot be lower than the start value");
						}
					},
					__("Enter Odometer Value"));
				}).addClass("btn-primary");
			}
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
	}
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