import Desktop from './components/Desktop.vue';

frappe.provide('frappe.views.pageview');

frappe.views.pageview = {
	show: function(name) {
		if(!name) {
			name = (frappe.boot ? frappe.boot.home_page : window.page_name);

			if(name === "desktop") {
				if(!frappe.pages.desktop) {
					let page = frappe.container.add_page('desktop');
					let container = $('<div class="container"></div>').appendTo(page);
					container = $('<div></div>').appendTo(container);

					new Vue({
						el: container[0],
						render: h => h(Desktop)
					});
				}

				frappe.container.change_to('desktop');
				frappe.utils.set_title(__('Bloomstack'));
				return;
			}
		}
		frappe.model.with_doctype("Page", function() {
			frappe.views.pageview.with_page(name, function(r) {
				if(r && r.exc) {
					if(!r['403'])
						frappe.show_not_found(name);
				} else if(!frappe.pages[name]) {
					new frappe.views.Page(name);
				}
				frappe.container.change_to(name);
			});
		});
	}
};