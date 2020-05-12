frappe.provide('frappe.contacts')

$.extend(frappe.contacts, {
	clear_address_and_contact: function (frm) {
		frm.fields_dict['address_html'] && $(frm.fields_dict['address_html'].wrapper).html("");
		frm.fields_dict['contact_html'] && $(frm.fields_dict['contact_html'].wrapper).html("");
	},

	render_address_and_contact: function (frm) {
		// render address
		if (frm.fields_dict['address_html'] && "addr_list" in frm.doc.__onload) {
			$(frm.fields_dict['address_html'].wrapper)
				.html(frappe.render_template("address_list",
					frm.doc.__onload))
				.find(".btn-address").on("click", function () {
					frappe.new_doc("Address");
				});
		}

		$(document).on('click', '.btn-address-link', function () {
			frappe.prompt({
				label: "Link Address",
				fieldname: "address",
				fieldtype: "Link",
				options: "Address",
				reqd: 1,
				get_query: () => {
					let addr_list = frm.doc.__onload.addr_list.map(addr => addr.name);
					return {
						filters: {
							"name": ["not in", addr_list]
						}
					}
				}
			},
				(data) => {
					frappe.call({
						method: "bloomstack_core.utils.link_address_or_contact",
						args: {
							"ref_doctype": "Address",
							"ref_name": data.address,
							"link_doctype": frm.doctype,
							"link_name": frm.docname
						},
						callback: function () {
							window.location.reload()
						}
					})
				}, __("Select Address"));
		})

		// render contact
		if (frm.fields_dict['contact_html'] && "contact_list" in frm.doc.__onload) {
			$(frm.fields_dict['contact_html'].wrapper)
				.html(frappe.render_template("contact_list",
					frm.doc.__onload))
				.find(".btn-contact").on("click", function () {
					frappe.new_doc("Contact");
				},
				);
		}

		$(document).on('click', '.btn-contact-link', function () {
			frappe.prompt({
				label: "Link Contact",
				fieldname: "contact",
				fieldtype: "Link",
				options: "Contact",
				reqd: 1,
				get_query: () => {
					let contact_list = frm.doc.__onload.contact_list.map(contact => contact.name);
					return {
						filters: {
							"name": ["not in", contact_list]
						}
					}
				}
			},
				(data) => {
					frappe.call({
						method: "bloomstack_core.utils.link_address_or_contact",
						args: {
							"ref_doctype": "Contact",
							"ref_name": data.contact,
							"link_doctype": frm.doctype,
							"link_name": frm.docname
						},
						callback: function () {
							window.location.reload()
						}
					})
				}, __("Select Contact"));
		})
	}
})