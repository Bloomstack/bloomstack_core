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

		$(document).on('click', '.address-box a.unlink_address', function () {
			var name = $(this).attr('data_address_name');
			frappe.confirm(
				'Are you sure you want to unlink this address linked with ' + cur_frm.docname + '?',
				function () {
					frappe.call({
						method: "bloomstack_core.utils.unlink_address_or_contact",
						args: {
							"ref_doctype": "Address",
							"ref_name": name,
							"doctype": cur_frm.doctype,
							"name": cur_frm.docname
						},
						callback: function () {
							window.location.reload()
						}
					})
				}
			);
		});

		$(document).on('click', '.address-box a.delete_address', function () {
			var name = $(this).attr('data_address_name');
			frappe.confirm(
				'If this address is linked to any other user in the system, it will just remove the address from ' + cur_frm.docname + '.<br> Are you sure you want to delete this address linked with ' + cur_frm.docname + '?',
				function () {
					frappe.call({
						method: "bloomstack_core.utils.delete_address_or_contact",
						args: {
							"ref_doctype": "Address",
							"ref_name": name,
							"doctype": cur_frm.doctype,
							"name": cur_frm.docname
						},
						callback: function () {
							window.location.reload()
						}
					})
				}
			);
		});

		// render contact
		if (frm.fields_dict['contact_html'] && "contact_list" in frm.doc.__onload) {
			$(frm.fields_dict['contact_html'].wrapper)
				.html(frappe.render_template("contact_list",
					frm.doc.__onload))
				.find(".btn-contact").on("click", function () {
					frappe.new_doc("Contact");
				}, );
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
		});

		$(document).on('click', '.address-box a.unlink_contact', function () {
			var name = $(this).attr('data_contact_name');
			frappe.confirm(
				'Are you sure you want to unlink this contact linked with ' + cur_frm.docname + '?',
				function () {
					frappe.call({
						method: "bloomstack_core.utils.unlink_address_or_contact",
						args: {
							"ref_doctype": "Contact",
							"ref_name": name,
							"doctype": cur_frm.doctype,
							"name": cur_frm.docname
						},
						callback: function () {
							window.location.reload()
						}
					})
				}
			);
		});

		$(document).on('click', '.address-box a.delete_contact', function () {
			var name = $(this).attr('data_contact_name');
			frappe.confirm(
				'If this contact is associated to any other user in the system, it will just remove the contact from ' + cur_frm.docname + '.<br> Are you sure you want to delete this contact linked with ' + cur_frm.docname + '?',
				function () {
					frappe.call({
						method: "bloomstack_core.utils.delete_address_or_contact",
						args: {
							"ref_doctype": "Contact",
							"ref_name": name,
							"doctype": cur_frm.doctype,
							"name": cur_frm.docname
						},
						callback: function () {
							window.location.reload()
						}
					})
				}
			);
		});

	}
})