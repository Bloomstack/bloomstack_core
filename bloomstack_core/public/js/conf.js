
frappe.provide('bloomstack_core');

// disable change log popups from frappe / erpnext
frappe.boot.change_log = []

// add toolbar icon
$(document).bind('toolbar_setup', () => {
	frappe.app.name = "Bloomstack";

	const $logo = $('<img class="erpnext-icon"/>')
		.attr('src', '/assets/bloomstack_core/images/icon.png');

	$('.navbar-home').empty().append($logo);

	//////////////////////////////////////////////////
	// BUILDING THE HELP MENU

	const $article_links = $(".dropdown-help #help-links");
	const $help_menu = $('.dropdown-help ul .documentation-links');

	// link to BCC laws and regulations
	const $bcc_site = $(`<li><a href="https://bcc.ca.gov/law_regs/" target="_blank">${__('BCC Guidelines')}</a></li>`)
		.insertAfter($help_menu)

	// replace Report Issue menu item
	const $report_issue_menu_item = $(`<li><a href="https://corp.bloomstack.com/issues" target="_blank">${__('Contact Support')}</a></li>`)
		// .click(report_issue)
		.insertAfter($bcc_site);

	// link to Growth Guide
	const $guide_menu_item = $(`<li><a href=${frappe.boot.growth_guide_link} target="_blank">${__('Growth Guide')}</a></li>`)
		.insertAfter($report_issue_menu_item);

	// Hack to remove all but the above elements
	$('.dropdown-help ul li')
		.not($bcc_site)
		.not($article_links)
		.not($help_menu)
		.not($guide_menu_item)
		.not($report_issue_menu_item)
		.remove();

	//////////////////////////////////////////////////

	function report_issue() {
		// adds erpnext email filter guard... cause... paranoid... :D
		const error_report_email = (frappe.boot.error_report_email || [])
			.filter(email => email.search('erpnext') === -1)
			.join(", ");

		const error_report_message = `
			<div style="min-height: 100px; border: 1px solid #bbb; \
			border-radius: 5px; padding: 15px; margin-bottom: 15px;">
				<h4>Site information:</h4>
				<ul>
					<li><strong>Current path:</strong> ${window.location.href}</li>
					<li><strong>Date: </strong>
						${frappe.datetime.global_date_format()},
						${frappe.datetime.now_time()},
						${Object.keys(frappe.boot.timezone_info.links)[0]}
					</li>
					<li><strong>Bloomstack version:</strong> ${frappe.boot.versions.bloomstack_core}</li>
				</ul>
			</div>
			<h4>What seems to be the problem?</h4>`;

		new frappe.views.CommunicationComposer({
			subject: "",
			recipients: error_report_email,
			message: error_report_message,
			doc: {
				doctype: "User",
				name: frappe.session.user
			}
		});

		return false;
	}
});

$(document).on("page-change", () => {
	const [view, doc_type, doc_name] = frappe.get_route();

	bloomstack_core.get_growth_guide_articles(doc_type);
	bloomstack_core.update_item_column_label(view, doc_type);
})

// replace Item link field label throughout the system from
// "item_code: item_name" to "item_name: item_code";
// original definition in ERPNext's utils.js file
frappe.form.link_formatters['Item'] = (value, doc) => {
	if (doc && doc.item_name && doc.item_name !== value) {
		return value
			? doc.item_name + ': ' + value
			: doc.item_name;
	} else {
		return value;
	}
}


frappe.form.link_formatters['Employee'] = function(value, doc) {
	if(doc && doc.employee_name) {
		return doc.employee_name;
	}
	if (doc && !doc.employee_name) {
		frappe.db.get_value("Employee", { "name" : value }, "employee_name", (r) => {
			employee_name = r.employee_name;
		});
		return employee_name;
	}
	else {
		return value;
	}
}

bloomstack_core.get_growth_guide_articles = (doc_type) => {
	frappe.call({
		method: "bloomstack_core.config.docs.get_growth_guide_articles",
		args: {
			"doc_type": doc_type || ""
		},
		callback: (r) => {
			if (!r.exc) {
				// Empty out existing article links and append results
				let $article_links = $(".dropdown-help #help-links").empty();

				for (let article of r.message) {
					$("<a>", {
						href: article.route,
						text: article.name,
						target: "_blank"
					}).appendTo($article_links);
				}
			}
		}
	})
}

bloomstack_core.update_item_column_label = (view, doc_type) => {
	if (view == "Form" && doc_type) {
		frappe.ui.form.on(doc_type, {
			onload_post_render: (frm) => {
				update_link_column_label(frm, "Item", "Item");
			}
		});
	}
}

bloomstack_core.add_login_as_button = (frm, label, user, submenu) => {
	// only one of these roles is allowed to use these feature
	if (frappe.user.has_role(["Administrator", "Can Login As", "System Manager"])) {
		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "User",
				name: user,
			},
			callback: (data) => {
				const user_doc = data.message;
				// only administrator can login as system user
				if (!frappe.user.has_role("Administrator") && user_doc && user_doc.user_type == "System User") {
					return;
				}

				if (user_doc) {
					frm.add_custom_button(label, () => {
						frappe.call({
							method: "bloomstack_core.utils.login_as",
							args: { user: user },
							freeze: true,
							callback: (data) => {
								window.location = "/desk";
							}
						})
					}, submenu);
				}
			}
		})
	}
}

function update_link_column_label(frm, link_doctype, label) {
	const table_doctypes = frappe.meta.get_table_fields(frm.doc.doctype)
		.filter(df => frappe.meta.get_linked_fields(df.options).includes(link_doctype))
		.map(df => df.options);

	for (let cdt of table_doctypes) {
		let cdt_obj = frm.grids.find(dt => dt.grid.doctype == cdt);
		let visible_columns = cdt_obj.grid.visible_columns;

		if (visible_columns) {
			for (let [column, column_length] of visible_columns) {
				if (column.fieldtype == "Link" && column.options == link_doctype) {
					let column_obj = cdt_obj.$wrapper.find(".grid-heading-row").find(`[data-fieldname=${column.fieldname}]`);
					column_obj.text(label);
				}
			}
		}
	}
}
