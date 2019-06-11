frappe.ui.form.on('Delivery Trip', {
    refresh: (frm) => {
        if (frm.doc.docstatus == 1 && frm.doc.status != "Completed" && frm.doc.odometer_start_value == 0) {
            frm.add_custom_button(__("Start"), () => {
                frappe.prompt([{
                    "label": "Odometer Start Value",
                    "fieldtype": "Int",
                    "fieldname": "odometer_start_value",
                    "reqd": 1
                },
                ],
                    function (data) {
                        frappe.call({
                            method: "bloomstack_core.utils.update_odometer",
                            args: {
                                "start": data.odometer_start_value,
                                "dn": frm.docname,
                            },
                        });
                    },
                    __("Enter Odometer Value"));

            }).addClass("btn-primary");
        }
        else if (frm.doc.docstatus == 1 && frm.doc.status != "Completed" && frm.doc.odometer_start_value > 0 && frm.doc.odometer_stop_value == 0) {
            frm.add_custom_button(__("Stop"), () => {
                frappe.prompt([{
                    "label": "Odometer Stop Value",
                    "fieldtype": "Int",
                    "fieldname": "odometer_stop_value",
                    "reqd": 1
                },
                ],
                    function (data) {
                        frappe.call({
                            method: "bloomstack_core.utils.update_odometer",
                            args: {
                                "stop": data.odometer_stop_value,
                                "dn": frm.docname,
                            },

                        });
                    },
                    __("Enter Odometer Value"));

            }).addClass("btn-primary");
        }
    }
});