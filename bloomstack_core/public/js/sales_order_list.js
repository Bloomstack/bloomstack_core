frappe.listview_settings['Sales Order'] = {
	add_fields: ["base_grand_total", "customer_name", "currency", "delivery_date",
		"per_delivered", "per_billed", "status", "order_type", "name", "skip_delivery_note"],
	get_indicator: function (doc) {
		if (doc.status === "Closed") {
			// Closed
			return [__("Closed"), "green", "status,=,Closed"];
		} else if (doc.status === "On Hold") {
			// on hold
			return [__("On Hold"), "orange", "status,=,On Hold"];
		} else if (doc.status === "Completed") {
			return [__("Completed"), "green", "status,=,Completed"];
		} else if (!doc.skip_delivery_note && flt(doc.per_delivered, 6) < 100) {
			if (frappe.datetime.get_diff(doc.delivery_date) < 0) {
				// not delivered & overdue
				return [__("Overdue"), "red",
					"per_delivered,<,100|delivery_date,<,Today|status,!=,Closed"];
			} else if (flt(doc.grand_total) === 0) {
				// not delivered (zero-amount order)
				return [__("To Deliver"), "orange",
					"per_delivered,<,100|grand_total,=,0|status,!=,Closed"];
			} else if (flt(doc.per_billed, 6) < 100) {
				// not delivered & not billed
				return [__("To Deliver and Bill"), "orange",
					"per_delivered,<,100|per_billed,<,100|status,!=,Closed"];
			} else {
				// not billed
				return [__("To Deliver"), "orange",
					"per_delivered,<,100|per_billed,=,100|status,!=,Closed"];
			}
		} else if ((flt(doc.per_delivered, 6) === 100) && flt(doc.grand_total) !== 0
			&& flt(doc.per_billed, 6) < 100) {
			// to bill
			return [__("To Bill"), "orange",
				"per_delivered,=,100|per_billed,<,100|status,!=,Closed"];
		} else if (doc.skip_delivery_note && flt(doc.per_billed, 6) < 100) {
			return [__("To Bill"), "orange", "per_billed,<,100|status,!=,Closed"];
		}
	},
	onload: function (listview) {
		var method = "erpnext.selling.doctype.sales_order.sales_order.close_or_unclose_sales_orders";

		listview.page.add_menu_item(__("Close"), function () {
			listview.call_for_selected_items(method, { "status": "Closed" });
		});

		listview.page.add_menu_item(__("Re-open"), function () {
			listview.call_for_selected_items(method, { "status": "Submitted" });
		});

		const action = () => {
			const selected_docs = listview.get_checked_items();
			const docnames = listview.get_checked_items(true);
			console.log(selected_docs);

			if (selected_docs.length > 0) {
				for (let doc of selected_docs) {
					if (doc.docstatus !== 1 || ["On Hold", "Closed"].includes(doc.status)) {
						frappe.throw(__("Cannot create a Pick List from {0} orders", [doc.status.bold()]));
					}
				};

				frappe.confirm(__("This action will create a Pick List for each Sales Order.<br><br>Are you sure you want to create {0} Pick List(s)?", [selected_docs.length]),
					() => {
						frappe.call({
							method: "bloomstack_core.hook_events.sales_order.create_multiple_pick_lists",
							args: {
								"orders": docnames
							},
							freeze: true,
							callback: (r) => {
								if (!r.exc) {
									if (r.message.length > 0) {
										console.log("SUCCESS: ", r);
									} else {
										console.log("FAIL: ", r);
									}

									frappe.msgprint(__(``));
									listview.refresh();
								}
							}
						});
					})
			};
		};

		listview.page.add_actions_menu_item(__('Create Pick Lists'), action, false);
	}
};