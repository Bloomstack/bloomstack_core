frappe.pages['license-search'].on_page_load = function(wrapper) {
	new frappe.views.LicenseSearchFactory().make('license-search');
}

frappe.views.LicenseSearchFactory = class LicenseSearchFactory extends frappe.views.Factory {
	make(page_name) {
		const assets = [
			'/assets/js/license_search.min.js',
			'/assets/css/license_search.min.css'
		];

		frappe.require(assets, () => {
			bloomstack_core.license_seach = new bloomstack_core.license_seach({
				parent: this.make_page(true, page_name)
			});
		});
	}
};

