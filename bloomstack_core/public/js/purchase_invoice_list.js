frappe.listview_settings['Purchase Invoice'].onload =
    function (doclist) {
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
                        frappe.throw(__("Select only one Supplier's purchase invoice"))
                    }
                };
                frappe.call({
                    method: "erpnext.utils.get_contact",
                    args: { "doctype": doctype, "name": selected_docs[0].name, "contact_field": "supplier" },
                    callback: function (r) {
                        frappe.call({
                            method: "erpnext.utils.get_document_links",
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
        doclist.page.add_actions_menu_item(__('Email'), action, true);
    }

