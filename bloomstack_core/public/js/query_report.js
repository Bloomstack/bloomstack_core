frappe.provide('frappe.views');
frappe.provide('bloomstack_core.customizations');


bloomstack_core.customizations.QueryReport = {
	originalRefresh: frappe.views.QueryReport.prototype.refresh,
	refresh(ctx, ...args) {
		// call original refresh function
		let queryPromise = this.originalRefresh.call(ctx, ...args);

		// hide the report's default no-data message and inject our spinner during the query
		ctx.toggle_message(false);
		frappe.dom.freeze("<img src='/assets/bloomstack_core/images/bloomstack_loader_infinity.svg'>");

		return queryPromise.then((result) => {
			this.cleanup();
			return result;
		}).catch((err) => {
			this.cleanup();
			throw err;
		});
	},
	cleanup() {
		// unfreeze the screen when query is complete
		if (frappe.dom.freeze_count > 0) {
			frappe.dom.unfreeze();
		}
	}
}

// wrap original code with our promise override
frappe.views.QueryReport.prototype.refresh = function (...args) {
	// passing "this" context to our override since we are taking over a prototype function
	return bloomstack_core.customizations.QueryReport.refresh(this, ...args);
}