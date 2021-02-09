/* eslint-disable */

frappe.pages["license-search"].on_page_load = function(wrapper) {
	let page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "License Search",
		single_column: true
	});

	frappe.require("assets/css/license_search.css", () => {
		new LicenseSearch({page: page});
	});
}

class LicenseSearch {
	constructor(opts) {
		$.extend(this, opts);
		this.limit_start = 0;
		this.limit_page_length = this.total_count = 21;
		this.license_types = []
		this.license_dict = {};
		this.licenses = [];
		this.make();
	}

	make() {
		let me = this;
		frappe.xcall("bloomstack_core.bloomstack_core.page.license_search.license_search.get_license_types").then((r) => {
			me.license_types = r;

			me.frm = new frappe.ui.FieldGroup({
				fields: me.get_fields(),
				body: me.page.wrapper.find(".layout-main-section-wrapper"),
				no_submit_on_enter: true
			});
			me.frm.make();
			me.show_totals_section();
			me.show_totals(true);
			me.show_placeholder()
			this.refresh()
		});
	}

	refresh() {
		let me = this;

		me.show_totals(true);
		frappe.xcall("bloomstack_core.bloomstack_core.page.license_search.license_search.get_all_licenses", {
			filters: me.frm.get_values(),
			limit_start: me.limit_start,
			limit_page_length: me.limit_page_length
		}).then((r) => {
			me.licenses = r.licenses;
			me.total_count = r.total_count;
			me.show_totals();
			me.show_licenses();
			me.set_license_card_actions();
			me.paginate();
		});
	}

	show_placeholder() {
		let me = this;
		let licenses_html = me.frm.get_field("licenses");
		let count = 0;

		let placeholders = []

		while (count < 6) {
			placeholders.push(`
				<div class="form-column card-padding col-sm-4">
					<div class="card card-padding">
						<div class="card-body row p-15">
							<div class="col-sm-12 h-25px bg-color rounded mb-10"></div>
							<div class="col-sm-12 h-25px bg-color rounded mb-10"></div>
							<div class="col-sm-12 h-25px bg-color rounded mb-10"></div>
							<div class="col-sm-12 h-25px bg-color rounded mb-10"></div>
							<div class="col-sm-12 h-25px bg-color rounded mb-10"></div>
							<div class="col-sm-12 h-25px bg-color rounded"></div>
						</div>
						<ul class="list-group-item p-0 no-border">
							<li class="list-group-item-no-border p-0"><hr></li>
							<li class="list-group-item-no-border pt-0 text-muted">Convert to</li>
							<li class="list-group-item-no-border">
								<div class="d-flex justify-content-between">
									<button type="button" class="btn btn-secondary" data-doctype="Customer" disabled>Customer</button>
									<button type="button" class="btn btn-secondary" data-doctype="Supplier" disabled>Supplier</button>
								</div>
							</li>
						</ul>
					</div>
				</div>
			`);
			count +=1;
		}

		licenses_html.$wrapper.html(`
			<div class="row">
				${placeholders.join("")}
			</div>
		`);
	}

	show_totals_section() {
		let me = this;
		let totals_html = me.frm.get_field("totals");

		totals_html.$wrapper.html(`
			<div class="row">
				<div class="col-sm-4 col-sm-offset-8">
					<p class="pull-right totals"></p>
				</div>
			</div>
		`);
	}

	show_totals(refreshing) {
		let me = this;
		let totals_html = me.frm.get_field("totals");
		let $wrapper = totals_html.$wrapper.find(".totals");
		let cards_range_start = me.limit_start;
		let cards_range_end = me.limit_start + me.limit_page_length;

		if (me.licenses.length === 0 && !refreshing) {
			$wrapper.html(``);
			return;
		}

		if (refreshing) {
			$wrapper.html(`
				<p class="text-muted">
					<img src="/assets/bloomstack_core/images/bloomstack_loader_infinity.svg" width="20px" height="20px"> Refreshing
				</p>
			`);
			return;
		}

		$wrapper.html(`<p class="text-muted">${cards_range_start} -
			${(cards_range_end >= me.total_count ? me.total_count : cards_range_end)}
			of ${me.total_count}</p>`);
	}

	show_licenses() {
		let me = this;
		let license_cards = [];

		if (me.licenses.length === 0) {
			license_cards.push(me.get_empty_state());
		} else {
			me.licenses.forEach(license => {
				me.add_to_dict(license)
				license_cards.push(me.get_license_card(license));
			});
		}

		let licenses_html = me.frm.get_field("licenses");
		licenses_html.$wrapper.html(`
			<div class="row">
				${license_cards.join("")}
			</div>
		`);
	}

	get_license_card(license) {
		let me = this;

		let card = `
			<div class="form-column card-padding col-sm-4">
				<div class="card card-padding">
					<div class="card-body">
						<h4 class="card-title">${license.legal_name.length > 25 ? license.legal_name.substring(0, 25) + "..." : license.legal_name}</h4>
						<hr>
						<p class="card-text">${license.license_number}</p>
						<p class="card-text">${license.license_type}</p>
						<p class="card-text">Address: ${me.get_address(license.city, license.county, license.zip_code) || "N/A"}</p>
						<p class="card-text">Email: ${license.email_id || "N/A"}</p>
						<p class="card-text">Expiry: ${license.expiration_date || "N/A"}</p>
						<p class="card-text">Status: ${license.status || "N/A"}</p>
						<hr>
					</div>
					<ul class="list-group-item p-0 no-border">
						<li class="list-group-item-no-border pt-0">Convert to</li>
						<li class="list-group-item-no-border">
							<div class="d-flex justify-content-between">
								<button type="button" class="btn btn-primary" data-doctype="Customer" data-license="${license.license_number}">Customer</button>
								<button type="button" class="btn btn-primary" data-doctype="Supplier" data-license="${license.license_number}">Supplier</button>
							</div>
						</li>
					</ul>
				</div>
			</div>
		`;
		return card;
	}

	get_empty_state() {
		return `
			<div class="text-center text-muted empty-state">
				${__("No Licenses found.")}
			</div>
		`
	}

	set_license_card_actions() {
		let me = this;
		let doctypes = ["Customer", "Supplier"];

		doctypes.forEach(dt => {
			me.page.wrapper.on("click", `button[data-doctype="${dt}"]`, function(el) {
				el.stopImmediatePropagation();
				el.preventDefault();
				let doctype = el.currentTarget.getAttribute("data-doctype");
				let license = el.currentTarget.getAttribute("data-license");
				me.create_document(doctype, me.license_dict[license]);
			});
		});
	}

	paginate() {
		let me = this;
		let pagination_html = me.frm.get_field("pagination");
		let $filters = me.frm.get_field("filters").$wrapper;

		if (me.licenses.length === 0 || me.licenses.length <= me.limit_page_length) {
			pagination_html.$wrapper.html(``);
			return;
		}

		pagination_html.$wrapper.html(`
			<div class="row">
				<div class="col-sm-12 text-center">
					<button type="button" class="btn btn-secondary" data-action="Prev">Prev</button>
					<button type="button" class="btn btn-secondary" data-action="Next">Next</button>
				</div>
			</div>
		`);

		pagination_html.$wrapper.find("button[data-action='Prev']").on("click", () => {
			if (me.limit_start > 0) {
				me.limit_start -= me.limit_page_length;
				frappe.utils.scroll_to($filters)
				me.refresh()
			}
		});

		pagination_html.$wrapper.find("button[data-action='Next']").on("click", () => {
			if (me.limit_start < me.total_count) {
				me.limit_start += me.limit_page_length;
				frappe.utils.scroll_to($filters)
				me.refresh()
			}
		});
	}

	create_document(doctype, license) {
		let me = this;

		let d = new frappe.ui.Dialog({
			title: __("Select Company"),
			fields: [
				{
					label: __("Company"),
					fieldtype: "Link",
					fieldname: "company",
					options: "Company",
					reqd: 1
				}
			],
			primary_action: function() {
				d.hide();
				let values = d.get_values();
				frappe.show_alert({
					message: __("Saving License {0}", [license.license_number]),
					indicator: "blue"
				});
				frappe.xcall("bloomstack_core.bloomstack_core.page.license_search.license_search.add_license", {
					license: license,
					company: values.company
				}).then(r => {
					frappe.show_alert({
						message: __("Saved"),
						indicator: "green"
					});

					frappe.model.open_mapped_doc({
						method: "bloomstack_core.bloomstack_core.page.license_search.license_search.create_party_with_license",
						args: {
							party: doctype,
							license: {
								license: r
							}
						}
					});
				});
			}
		});

		d.show();
	}

	get_address(city, country, zip_code) {
		let address = [];

		if (city) address.push(city);
		if (country) address.push(country);
		if (zip_code) address.push(zip_code);

		return address.join(" | ");
	}

	add_to_dict(license) {
		this.license_dict[license.license_number] = license;
	}

	filters_refresh() {
		let me = this;
		me.limit_start = 0;
		me.refresh()
	}

	get_fields() {
		let me = this;

		return [
			{
				fieldtype: "Section Break",
				fieldname: "filters"
			},
			{
				label: __("License Type"),
				fieldtype: "Select",
				fieldname: "license_type",
				options: me.get_license_types(),
				onchange: () => me.filters_refresh()
			},
			{
				fieldtype: "Column Break"
			},
			{
				label: __("Legal Name"),
				fieldtype: "Data",
				fieldname: "legal_name",
				onchange: () => me.filters_refresh()
			},
			{
				fieldtype: "Column Break"
			},
			{
				label: __("Zipcode"),
				fieldtype: "Data",
				fieldname: "zip_code",
				onchange: () => me.filters_refresh()
			},
			{
				fieldtype: "Section Break"
			},
			{
				fieldtype: "HTML",
				fieldname: "totals"
			},
			{
				fieldtype: "HTML",
				fieldname: "licenses"
			},
			{
				fieldtype: "HTML",
				fieldname: "pagination"
			}
		]
	}

	get_license_types() {
		return this.license_types;
	}
}
