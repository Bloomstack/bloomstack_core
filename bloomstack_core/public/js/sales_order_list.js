frappe.listview_settings['Sales Order'] = {
    onload: function (doclist) {
        console.log("Hi");
		const action = () => {
			const selected_docs = doclist.get_checked_items();
            const docnames = doclist.get_checked_items(true);

			if (selected_docs.length > 0) {
				for (let doc of selected_docs) {
					if (doc.docstatus !== 1 || doc.is_return) {
						frappe.throw(__("Cannot create a Delivery Note from 'Cancelled', 'Draft' or 'Return' Sales Order."));
					}
				};
                frappe.call({
                    method: "bloomstack_core.utils.create_delivery_notes",
                    args: {
                        "source_names": docnames,
                    },
                    callback: function (r) {
                        let l = []
                        for (let each of r.message) {
                            l.push(each.name);
                        }
                        let l_string = l.join();
                        frappe.msgprint(__("The Delivery Notes", l_string, "have been created!"));
                    }
                });
			};
		};
		doclist.page.add_actions_menu_item(__('Create Delivery Notes'), action, false);
	}
};