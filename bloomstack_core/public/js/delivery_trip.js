frappe.ui.form.on('Delivery Trip', {
	refresh: (frm) => {
        if (frm.doc.status == "Scheduled" && frm.doc.odometer_start != 0){
           
            frm.add_custom_button(__("Start"), () => {
                console.log("yupup")
                frappe.prompt([{
                    "label": "Initial Reading",
                    "fieldtype": "Float",
                    "fieldname": "odometer_start",
                    "reqd": 1
                },
            ],
                function (data) {
                    console.log("data.odometer_start", data.odometer_start, "docname", frm.docname)

                    frappe.call({
                        method: "bloomstack_core.utils.update_odometer",
                        args: {
                            "start": data.odometer_start,
                            "dn": frm.docname,
                        },
                    })
                    },
                __("Enter Odometer Value"));

            }).addClass("btn-primary");
        }
        else {
            frm.add_custom_button(__("Stop"), () => {
                console.log("yupup")
                frappe.prompt([{
                    "label": "Final Reading",
                    "fieldtype": "Float",
                    "fieldname": "odometer_stop",
                    "reqd": 1
                },
            ],
                function (data) {
                    console.log("data.odometer_stop", data.odometer_stop, "docname", frm.docname)

                    frappe.call({
                        method: "bloomstack_core.utils.update_odometer",
                        args: {
                            "stop": data.odometer_stop,
                            "dn": frm.docname,
                        },
                    })
                    },
                __("Enter Odometer Value"));

            }).addClass("btn-primary");
        };

    }
});