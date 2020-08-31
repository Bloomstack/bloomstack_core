frappe.pages['admin_insights'].on_page_load = function(wrapper) {
	new frappe.views.InsightsFactory().make('admin_insights');
	// var page = frappe.ui.make_app_page({
	// 	parent: wrapper,
	// 	title: 'Admin Insights',
	// 	single_column: true
	// });
}

frappe.views.InsightsFactory = class InsightsFactory extends frappe.views.Factory {
	make(page_name) {
		const assets = [
			'assets/bloomstack_core/js/min/admin_insights.min.js',
			// 'assets/bloomstack_core/css/admin_insights.css'
		];

		frappe.require(assets, () => {
			bloomstack_core.insights = new bloomstack_core.insights({
				parent: this.make_page(true, page_name)
			});
		});
	}
};