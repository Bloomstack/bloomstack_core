frappe.pages['admin_insights'].on_page_load = function(wrapper) {
	console.log("hello");
	new frappe.views.InsightsFactory().make('admin_insights');
	// var page = frappe.ui.make_app_page({
	// 	parent: wrapper,
	// 	title: 'Admin Insights',
	// 	single_column: true
	// });
}

frappe.views.InsightsFactory = class InsightsFactory extends frappe.views.Factory {
	make(page_name) {
		console.log("hola main bola!");
		const assets = [
			'assets/bloomstack_core/js/min/admin_insights.min.js'
		];

		console.log("namaste memsahab");
		frappe.require(assets, () => {
			console.log(bloomstack_core.admin_insights);
			const say_what = new bloomstack_core.admin_insights({
				parent: this.make_page(true, page_name)
			});
		});
	}
};