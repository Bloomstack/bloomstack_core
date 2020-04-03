frappe.ui.form.on("Lead", {
	setup: (frm) => {
		frm.set_query("region", { "is_group": 1 });
	},
	refresh: function(frm){
		frappe.custom_contacts.render_address_and_contact(frm)
	},
	onload: function(frm) {
		frm.set_query("custom_territory", () => {
			if (frm.doc.region) {
				return {
					query: "bloomstack_core.hook_events.lead.filter_territory",
					filters: {
						region: frm.doc.region
					}
				}
			}
		});

		if(frm.doc.status == 'Converted') {
			frappe.db.get_value("Customer", {"lead_name": frm.doc.name}, "creation", (r) => {
				if(r) {
					frm.set_value("account_opened_date", r.creation);
				}	
			});

	  }

	},
	//As standard field not allowed to re-arrange we update with custom field
	custom_territory: function(frm){
		frm.set_value("territory", frm.doc.custom_territory);
	},
	custom_contact_by: function(frm){
		frm.set_value("contact_by", frm.doc.custom_contact_by);
	}
});

frappe.provide('frappe.custom_contacts')

$.extend(frappe.custom_contacts, {
	render_address_and_contact: function(frm) {
		// render address
		if(frm.fields_dict['custom_address_html'] && "addr_list" in frm.doc.__onload) {
			$(frm.fields_dict['custom_address_html'].wrapper)
				.html(frappe.render_template("address_list",
					frm.doc.__onload))
				.find(".btn-address").on("click", function() {
					frappe.new_doc("Address");
				});
		}

		// render contact
		if(frm.fields_dict['custom_contact_html'] && "contact_list" in frm.doc.__onload) {
			$(frm.fields_dict['custom_contact_html'].wrapper)
				.html(frappe.render_template("contact_list",
					frm.doc.__onload))
				.find(".btn-contact").on("click", function() {
					frappe.new_doc("Contact");
				}
			);
		}
	}
})