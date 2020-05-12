frappe.listview_settings['Sales Order'].onload = function (doclist) {
	const create_pick_list_action = () => {
		const selected_docs = doclist.get_checked_items();
		const docnames = doclist.get_checked_items(true);

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

								} else {

								}

								frappe.msgprint(__(``));
								doclist.refresh();
							}
						}
					});
				})
		};
	};

	doclist.page.add_actions_menu_item(__('Create Pick Lists'), create_pick_list_action, false);

	const send_email_action = () => {
		const selected_docs = doclist.get_checked_items();
		const doctype = doclist.doctype;
		if (selected_docs.length > 0) {
			let title = selected_docs[0].title;
			for (let doc of selected_docs) {
				if (doc.docstatus !== 1) {
					frappe.throw(__("Cannot Email Draft or cancelled documents"));
				}
				if (doc.title !== title) {
					frappe.throw(__("Select only one customer's sales orders"))
				}
			};
			frappe.call({
				method: "bloomstack_core.utils.get_contact",
				args: { "doctype": doctype, "name": selected_docs[0].name, "contact_field": "customer" },
				callback: function (r) {
					frappe.call({
						method: "bloomstack_core.utils.get_document_links",
						args: { "doctype": doctype, "docs": selected_docs },
						callback: function (res) {
							new frappe.views.CommunicationComposer({
								subject: `${frappe.sys_defaults.company} - ${doctype} links`,
								recipients: r.message ? r.message.email_id : null,
								message: res.message,
								doc: {}
							})
						}
					})
				}
			})
		}
	}
	doclist.page.add_actions_menu_item(__('Email'), send_email_action, true);
}
