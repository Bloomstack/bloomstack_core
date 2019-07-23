frappe.ui.form.on("Contract", {
    refresh: (frm) => {
        // Make "Signed" field read-only if a project is created against it
        frm.toggle_enable("is_signed", !(frm.doc.is_signed && frm.doc.project));

        if (!frm.is_new() && frm.doc.docstatus === 0) {
            if (!frm.doc.customer_signature) {
                frm.add_custom_button(__("Authorize"), () => {
                    frappe.prompt([
                        {
                            "label": "Contact Email",
                            "fieldtype": "Data",
                            "options": "Email",
                            "fieldname": "contact_email",
                            "default": frm.doc.party_user,
                            "reqd": 1
                        },
                        {
                            "label": "Contact Person",
                            "fieldtype": "Data",
                            "fieldname": "contact_person",
                            "default": frm.doc.party_name
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
                                    frappe.msgprint(__(`${frm.doc.name} has been successfully sent to ${data.contact_email}`))
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