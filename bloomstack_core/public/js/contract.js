frappe.ui.form.on("Contract", {
    refresh: (frm) => {
        // pull users for the set party
        frm.set_query("party_user", (doc) => {
            return {
                query: "bloomstack_core.hook_events.contract.get_party_users",
                filters: {
                    "party_type": doc.party_type,
                    "party_name": doc.party_name
                }
            }
        });

        if (frm.doc.docstatus === 1 && !frm.doc.customer_signature) {
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
                        "default": frm.doc.party_name,
                        "reqd": 1
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
    },

    before_submit: (frm) => {
        if(!frm.doc.signee_company) {
            frm.scroll_to_field('signee_company');
            frappe.throw("Please sign the contract before submiting it.")
        }
    },

    party_name: (frm) => {
        if(frm.doc.party_type == 'Employee') {
            frappe.db.get_value("Employee", { "name": frm.doc.party_name }, "employee_name", (r) => {
                frm.doc.employee_name = r.employee_name; 
                frm.refresh_field("employee_name");
            })
        }
    },
    
});
