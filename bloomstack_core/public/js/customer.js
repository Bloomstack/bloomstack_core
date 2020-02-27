frappe.ui.form.on("Customer", {
	setup: (frm) => {
		frm.set_query("territory", { "is_group": 0 });
	},

	refresh: (frm) => {
		if (!frm.is_new()) {
			frm.add_custom_button(__("License Info"), () => {
				frappe.set_route("List", "Compliance Info", { "entity": frm.doc.name })
			})
		}
	},
	validate:function(doc){
		return validateCustomerWindow(doc); 
	},
})

function validateCustomerWindow(frm) {
	if (frm.doc.delivery_start_time > frm.doc.delivery_stop_time) {
		return frappe.throw(__(`Customer start window: ${frm.doc.delivery_start_time} should be before Customer end window:${frm.doc.delivery_stop_time}`))
	}
}
