frappe.listview_settings['Purchase Order'] = {
    onload: function (doclist) {
        const action = () => {
            const selected_docs = doclist.get_checked_items();
            const doctype = doclist.doctype;
            if (selected_docs.length > 0) {
                let title = selected_docs[0].title;
                for (let doc of selected_docs) {
                    if (doc.docstatus !== 1) {
                        frappe.throw(__("Cannot Email Draft or cancelled documents"));
                    }
                    if (doc.title !== title) {
                        frappe.throw(__("Select only one Supplier's purchase orders"))
                    }
                };
                frappe.call({
                    method: "bloomstack_core.hook_events.purchase_order.get_contact",
                    args: { "name": selected_docs[0].name, doctype: doctype },
                    callback: function (r) {
                        frappe.call({
                            method: "bloomstack_core.hook_events.purchase_order.get_attach_link",
                            args: { docs: selected_docs, doctype: doctype },
                            callback: function (res) {
                                new frappe.views.CommunicationComposer({
                                    subject: frappe.sys_defaults.company + " " + doctype + " links",
                                    recipients: r.message ? r.message.contact_person.email_id : null,
                                    message: res.message,
                                    doc: {
                                        doctype: doctype,
                                        name: frappe.session.user
                                    }
                                })
                            }
                        })
                    }
                })
            }
        }
        doclist.page.add_actions_menu_item(__('Email'), action, true);
    }
}
