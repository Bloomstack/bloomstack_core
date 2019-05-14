frappe.ui.form.on('Quotation', {
    refresh: (frm) => {
        if (!frm.is_new() && frm.doc.docstatus === 0) {
            if (!frm.doc.customer_signature) {
                frm.add_custom_button(__("Authorize"), () => {
                    frappe.new_doc("Authorization Request", {
                        linked_doctype: frm.doc.doctype,
                        linked_docname: frm.doc.name,
                        signee_name: frm.doc.contact_person,
                        authorizer_email: frm.doc.contact_email
                    })
                }).addClass("btn-primary");

            }
        }
    },
    
});
