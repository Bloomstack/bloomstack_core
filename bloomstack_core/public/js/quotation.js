frappe.ui.form.on('Quotation', {
    refresh: (frm) => {
        if (!frm.is_new() && frm.doc.docstatus === 0) {
            if (!frm.doc.customer_signature) {
                frm.add_custom_button(__("Authorize"), () => {
                    frappe.prompt([
                        {
                            "label": "Contact Email",
                            "fieldtype": "Data",
                            "options": "Email",
                            "fieldname": "contact_email",
                            "default": frm.doc.contact_email,
                            "reqd": 1
                        },
                        {
                            "label": "Contact Person",
                            "fieldtype": "Data",
                            "fieldname": "contact_person",
                            "default": frm.doc.contact_person
                        }
                    ],
                    function (data) {
                        frappe.call({
                            method: "bloomstack_core.utils.create_authorization_request",
                            args: {
                                dt: frm.doc.doctype,
                                dn: frm.doc.name,
                                contact_email: data.contact_email,
                                contact_name: data.contact_person
                            },
                            callback: (r) => {
                                if (!r.exc) {
                                    frappe.msgprint(__(`The document ${frm.doc.name} has been successfully emailed to ${data.contact_person}`))
                                }
                            }
                        })
                    },
                    __("Send Authorization Request"))
                }).addClass("btn-primary");

            }
        }
    },
    
});
