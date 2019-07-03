frappe.ui.form.on('Delivery Trip', {
	refresh: (frm) => {
		if (frm.doc.docstatus == 1 && frm.doc.status != "Completed") {
			if (frm.doc.odometer_start_value == 0) {
				frm.add_custom_button(__("Start"), () => {
					frappe.prompt({
						"label": "Odometer Start Value",
						"fieldtype": "Int",
						"fieldname": "odometer_start_value",
						"reqd": 1
					},
					(data) => {
						frm.set_value('odometer_start_value', data.odometer_start_value);
						frm.set_value('odometer_start_time', frappe.datetime.now_datetime());
						frm.dirty();
						frm.save_or_update();
					},
					__("Enter Odometer Value"));
				}).addClass("btn-primary");
			} else if (frm.doc.odometer_start_value > 0 && frm.doc.odometer_stop_value == 0) {
				frm.add_custom_button(__("Stop"), () => {
					frappe.prompt({
						"label": "Odometer Stop Value",
						"fieldtype": "Int",
						"fieldname": "odometer_stop_value",
						"reqd": 1
					},
					(data) => {
						if (data.odometer_stop_value > frm.doc.odometer_start_value) {
							frm.set_value('odometer_stop_value', data.odometer_stop_value);
							frm.set_value('odometer_stop_time', frappe.datetime.now_datetime());
							frm.set_value('actual_distance_travelled', (data.odometer_stop_value - frm.doc.odometer_start_value));
							frm.dirty();
							frm.save_or_update();
						} else {
							frappe.throw("The stop value cannot be lower than the start value");
						}
					},
					__("Enter Odometer Value"));
				}).addClass("btn-primary");
			}
		}
	}
});