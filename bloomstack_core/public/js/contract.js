frappe.ui.form.on("Contract", {
    refresh: (frm) => {
        if (!frm.is_new() && frm.doc.docstatus === 0) {
            if (!frm.doc.customer_signature) {
                frm.add_custom_button(__("Authorize"), () => {
                    frappe.new_doc("Authorization Request", {
                        linked_doctype: frm.doc.doctype,
                        linked_docname: frm.doc.name,
                    })
                }).addClass("btn-primary");

            }
        }
    },
});