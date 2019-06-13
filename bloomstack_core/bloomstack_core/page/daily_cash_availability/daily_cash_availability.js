frappe.pages['daily-cash-availability'].on_page_load = (wrapper) => {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Daily Cash Availability',
		single_column: true
	});

	wrapper.sales_funnel = new bloomstack_core.DailyCashAvailability(wrapper);
	frappe.breadcrumbs.add("Accounts");
}

bloomstack_core.DailyCashAvailability = class DailyCashAvailability {
	constructor(wrapper) {
		this.setup(wrapper);
		this.get_data();
	}

	setup(wrapper) {
		let me = this;

		this.elements = {
			layout: $(wrapper).find(".layout-main"),
			refresh_btn: wrapper.page.set_primary_action(__("Refresh"), () => { me.get_data(); }, "fa fa-refresh"),
		};

		this.elements.no_data = $('<div class="alert alert-warning">' + __("No Data") + '</div>')
			.toggle(false)
			.appendTo(this.elements.layout);

		// bind refresh
		this.elements.refresh_btn.on("click", function () {
			me.get_data(this);
		});
	}

	get_data() {
		let me = this;
		frappe.call({
			method: "bloomstack_core.bloomstack_core.page.daily_cash_availability.daily_cash_availability.get_cash_in_hand_accounts",
			callback: function (r) {
				if (!r.exc && r.message) {
					const company = frappe.sys_defaults.company;
					const currency = frappe.get_doc(":Company", company).default_currency;
					const cash_in_hand_accounts = r.message;

					let html = "";
					let cash_in_hand = 0.0;
					for (let account in cash_in_hand_accounts) {
						cash_in_hand += cash_in_hand_accounts[account];
						html += `
							<div class="list-item_content ellipsis list-item__content--flex-2">
								<a class="grey list-id ellipsis" href = "#Form/Account/${account}"> ${account} </a>
							</div>
							<div class="list-item_content ellipsis list-item__content--flex-2 text-right">
								<span class="text-muted ellipsis"> ${format_currency(cash_in_hand_accounts[account], currency)}</span>
							</div>
						`
					}

					html += `<br><br>
						<div class="list-item_content ellipsis list-item__content--flex-2 text-right">
							<span class="text-muted ellipsis"> Total: ${format_currency(cash_in_hand, currency)}</span>
						</div>
					`

					const $parent = me.elements.layout;
					$parent.html(html);
				} else {
					me.elements.no_data.toggle(true);
				}
			}
		});
	}
}