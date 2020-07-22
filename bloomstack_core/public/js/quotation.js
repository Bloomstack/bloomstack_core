frappe.provide("bloomstack_core.utils");
frappe.ui.form.on('Quotation', {
	refresh: (frm) => {
		if (!frm.is_new() && frm.doc.docstatus === 0) {
			if (!frm.doc.customer_signature) {
				frm.add_custom_button(__("Authorize"), () => {
					frappe.prompt([
						{
							"label": "Contact Email",
							"fieldtype": "Data",
							"options": "Email",
							"fieldname": "contact_email",
							"default": frm.doc.contact_email,
							"reqd": 1
						},
						{
							"label": "Contact Person",
							"fieldtype": "Data",
							"fieldname": "contact_person",
							"default": frm.doc.contact_person,
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
									frappe.msgprint(__(`The document ${frm.doc.name} has been successfully emailed to ${data.contact_person}`))
								}
							}
						})
					},
					__("Send Authorization Request"))
				}).addClass("btn-primary");
			}
		}

		if (!frm.is_new() && frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Contract"), () => {
				frappe.model.open_mapped_doc({
					method: "bloomstack_core.utils.create_contract_from_quotation",
					frm: frm
				});
			}, __("Create"));
		}
	},
	onload: (frm) => {
		frm.set_query("license", () => {
			if (frm.doc.quotation_to === "Customer" && frm.doc.party_name) {
				return {
					query: "bloomstack_core.hook_events.utils.filter_license",
					filters: {
						party_name: frm.doc.party_name
					}
				};
			}
		});
	},
	party_name: (frm) => {
		if (frm.doc.quotation_to === "Customer" && frm.doc.party_name) {
			frappe.call({
				method: "bloomstack_core.hook_events.utils.validate_entity_license",
				args: {
					party_type: "Customer",
					party_name: frm.doc.party_name
				},
				callback: (r) => {
					if(r.message){
						frm.set_value("license", r.message)
					}
				}
			});

			// set excise tax if customer party has license number
			bloomstack_core.utils.set_and_update_excise_tax(frm);
		}
	},
	no_charge_order: (frm) => {
		frm.trigger("set_promotional_discount");
	},

	set_promotional_discount: (frm) => {
		let percentage_discount = 0;

		if (frm.doc.no_charge_order) {
			frm.set_value("apply_discount_on", "Grand Total");
			percentage_discount = 100;
		}

		frm.set_value("additional_discount_percentage", percentage_discount);

		frappe.show_alert({
			indicator: 'green',
			message: __(`${percentage_discount}% discount applied`)
		});
	},
	order_type: (frm) => {
		if (frm.doc.order_type) {
			bloomstack_core.utils.set_and_update_excise_tax(frm);
		}
	}
});
