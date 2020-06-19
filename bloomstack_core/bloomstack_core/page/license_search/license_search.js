frappe.pages['license-search'].on_page_load = function(wrapper) {
	new frappe.views.LicenseSearchFactory().make('license-search');
}

frappe.views.LicenseSearchFactory = class LicenseSearchFactory extends frappe.views.Factory {
	make(page_name) {
		const assets = [
			'assets/bloomstack_core/js/min/license_search.min.js',
			'assets/bloomstack_core/css/license_search.css'
		];

		frappe.require(assets, () => {
			bloomstack_core.license_seach = new bloomstack_core.license_seach({
				parent: this.make_page(true, page_name)
			});
		});
	}
};

