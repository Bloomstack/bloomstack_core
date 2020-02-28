frappe.ui.form.on("Supplier", {
	refresh: (frm) => {
		if (!frm.is_new()) {
			let contact_emails;
			frappe.xcall("bloomstack_core.hook_events.supplier.get_supplier_emails", {
				supplier: frm.doc.name
			}).then(r => {
				contact_emails = r.contact_emails;
			})

			// add email buttons to send Purchase Orders and Invoices
			frm.add_custom_button(__('Purchase Orders'), () => {
				email_documents("Purchase Order", frm.doc.name, contact_emails);
			}, __('Email'));

			frm.add_custom_button(__('Purchase Invoices'), () => {
				email_documents("Purchase Invoice", frm.doc.name, contact_emails);
			}, __('Email'));

			frm.add_custom_button(__("License Info"), () => {
				frappe.set_route("List", "Compliance Info", { "entity": frm.doc.name })
			});
		};
	}
})

const email_documents = (doctype, supplier, emails) => {
	if (!emails.length) {
		frappe.msgprint(__("Please set a contact with an email address for {0}", [supplier]));
		return;
	}

	let supplier_emails = emails.map(email => email.email);
	let primary_supplier_email = emails.find(email => email.is_primary == 1)

	frappe.xcall('bloomstack_core.utils.get_doctype_status_options', { "doctype": doctype })
		.then(options => {
			frappe.prompt([{
					label: "Recipient Email",
					fieldname: "email",
					fieldtype: "Select",
					options: supplier_emails,
					default: primary_supplier_email,
					reqd: 1
				},
				{
					label: "Status",
					fieldname: "status",
					fieldtype: "Select",
					options: options,
					reqd: 1
				},
				{
					label: "From Transaction Date",
					fieldname: "from_date",
					fieldtype: "Date",
					reqd: 1
				},
				{
					label: "To Transaction Date",
					fieldname: "to_date",
					fieldtype: "Date",
					reqd: 1
				}
			],
				(data) => {
					data.doctype = doctype;
					data.supplier = supplier;

					frappe.call({
						method: "bloomstack_core.hook_events.supplier.send_purchase_documents",
						args: data,
						freeze: true,
						callback: (r) => {
							if (r.exc) {
								frappe.msgprint(__("There was an error trying to send the documents. Please contact your administrator for more details."))
							}

							if (r.message) {
								if (!r.message.length) {
									frappe.msgprint(__("No {0}s found with those filters.", [doctype]))
								} else {
									frappe.msgprint(__("Email sent successfully to {0}", [email]))
								}
							}
						}
					});
				}, __("Filter {0}s", [doctype]), __("Email")
			);
		})
}