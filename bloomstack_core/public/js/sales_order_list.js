frappe.listview_settings['Sales Order'] = {
	onload: function (doclist) {
		const action = () => {
			const selected_docs = doclist.get_checked_items();
			const docnames = doclist.get_checked_items(true);

			if (selected_docs.length > 0) {
				for (let doc of selected_docs) {
					if (doc.docstatus !== 1) {
						frappe.throw(__("Cannot create a Delivery Note from 'Cancelled', 'Draft' Sales Order."));
					}
				};
				frappe.call({
					method: "bloomstack_core.utils.create_delivery_notes",
					args: {
						"source_names": docnames,
					},
					callback: function (r) {
						frappe.msgprint(__("The Delivery Notes " + r.message.join(", ") + " have been created!"));
					}
				});
			};
		};
		doclist.page.add_actions_menu_item(__('Create Delivery Notes'), action, false);
	}
};