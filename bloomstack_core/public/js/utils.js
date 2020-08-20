$(document).on('app_ready', function() {
	$.each(["Project", "Task", "Project Template", "Project Type"], function (i, doctype) {
		frappe.ui.form.on(doctype, {
			billable: (frm) => {
				let confirm_message = "";
				frappe.call({
					method: "bloomstack_core.hook_events.utils.get_linked_documents",
					args: {
						doctype: frm.doc.doctype,
						name: frm.doc.name
					},
					freeze: true,
					callback: (r) => {
						if (!r.exc && r.message.count > 0) {
							// add confirmation message for cancelling all linked docs
							let links_text = "";
							let links = r.message.docs;
							const doctypes = Array.from(new Set(links.map((link) => link.doctype)));

							for (let doctype of doctypes) {
								let docnames = links
									.filter((link) => link.doctype === doctype)
									.map((link) => frappe.utils.get_form_link(link.doctype, link.name, true))
									.join(", ");
								links_text += `<li><strong>${doctype}</strong>: ${docnames}</li>`;

							}
							links_text = "<ul>" + links_text + "</ul>";

							confirm_message = `${frm.doc.name.bold()} is linked with the following documents: ${links_text}`;
							frappe.confirm(__(`${confirm_message} Do you want to set them as <strong>{0}</strong> too?`, [frm.doc.billable ? "billable" : "non-billable"]),
								() => {
									frappe.call({
										method: "bloomstack_core.hook_events.utils.update_timesheet_logs",
										args: {
											ref_dt: frm.doctype,
											ref_dn: frm.doc.name,
											billable: frm.doc.billable
										},
										callback: (r) => {
											frm.save();
										}
									})
								},
								() => {
									frm.doc.billable = !frm.doc.billable;
									refresh_field("billable");
								}
							);
						}
					}
				});
			}
		});
	});
});
