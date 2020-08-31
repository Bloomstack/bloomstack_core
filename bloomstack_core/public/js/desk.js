import Desktop from './components/Desktop.vue';

frappe.provide('frappe.views.pageview');

frappe.views.pageview = {
	with_page: function(name, callback) {
		if(in_list(Object.keys(frappe.standard_pages), name)) {
			if(!frappe.pages[name]) {
				frappe.standard_pages[name]();
			}
			callback();
			return;
		}

		if((locals.Page && locals.Page[name] && locals.Page[name].script) || name==window.page_name) {
			// already loaded
			callback();
		} else if(localStorage["_page:" + name] && frappe.boot.developer_mode!=1) {
			// cached in local storage
			frappe.model.sync(JSON.parse(localStorage["_page:" + name]));
			callback();
		} else {
			// get fresh
			return frappe.call({
				method: 'frappe.desk.desk_page.getpage',
				args: {'name':name },
				callback: function(r) {
					if(!r.docs._dynamic_page) {
						localStorage["_page:" + name] = JSON.stringify(r.docs);
					}
					callback();
				},
				freeze: true,
			});
		}
	},
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