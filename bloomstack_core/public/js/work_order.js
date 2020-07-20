frappe.ui.form.on("Work Order", {
	setup: (frm) => {
		frappe.meta.docfield_map["Work Order Operation"].operation.formatter =
			function (value, df, options, doc) {
				if (!value) {
					return '';
				}

				let label;
				if (frappe.form.link_formatters[df.options]) {
					label = frappe.form.link_formatters[df.options](value, doc);
				} else {
					label = value;
				}

				let color;
				if (!doc.completed_qty) {
					color = "red";
				} else if (doc.completed_qty < frm.doc.qty) {
					color = "orange";
				} else if (doc.completed_qty == frm.doc.qty) {
					color = "green";
				}

				const escaped_name = encodeURIComponent(value);

				return repl('<a class="indicator %(color)s" href="#Form/%(doctype)s/%(name)s">%(label)s</a>', {
					color: color,
					doctype: df.options,
					name: escaped_name,
					label: label
				});
			};
	},
	// refresh: (frm) => {
	// 	frm.add_custom_button(__('Start Job Cards'), function(){
	// 		frappe.call({
	// 			method: "bloomstack_core.hook_events.work_order.start_job_cards",
	// 			args: {
	// 				doctype: frm.doc.doctype,
	// 				name: frm.doc.name
	// 			},
	// 			freeze: true,
	// 			callback: (r) => {
	// 				console.log("message", r);
	// 				if(!r.message.length){
	// 					frappe.msgprint("There is nothing open job card to start");
	// 				} else {
	// 					frappe.msgprint("Following Job card started");
	// 				}
	// 			}
	// 		})
	// 	}).addClass('btn-primary');
	// 	frm.add_custom_button(__('Stop Job Cards'), function(){
	// 		frappe.call({
	// 			method: "bloomstack_core.hook_events.work_order.stop_job_cards",
	// 			args: {
	// 				doctype: frm.doc.doctype,
	// 				name: frm.doc.name
	// 			},
	// 			freeze: true,
	// 			callback: (r) => {
	// 				console.log("message", r.message)
	// 				if(!r.message.length){
	// 					frappe.msgprint("There is nothing open job card to stop");
	// 				} else {
	// 					frappe.msgprint("Following Job card stoped");
	// 				}
	// 			}
	// 		})
	// 	}).addClass('btn-primary');
	// }
});
