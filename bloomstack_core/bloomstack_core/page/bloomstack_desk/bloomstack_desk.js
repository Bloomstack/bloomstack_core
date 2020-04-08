{% include "bloomstack_core/bloomstack_core/page/bloomstack_desk/bloomstack_desk.html" %}

frappe.pages['bloomstack_desk'].on_page_load = function(wrapper) {
	// var page = frappe.ui.make_app_page({
	// 	parent: wrapper,
	// 	title: 'None',
	// 	single_column: true
	// });
	wrapper.bloomstackdesk = new BloomstackDesk(wrapper);
}

class BloomstackDesk {
	constructor(parent) {
		frappe.ui.make_app_page({
			parent: parent,
			title: 'Bloomstack Desk',
			single_column: true
		});
		const assets = [
			'assets/bloomstack_core/css/bloomdesk.css'
		];

		frappe.require(assets, () => {
			this.make();
		});

		this.elements = {
			page: parent.page,
			parent: $(parent).find(".layout-main"),
		};
	}
	make() {
		this.renderPage();
		this.animate();
	}
	


	renderPage() {
	
		let html = frappe.render_template("bloomstack_desk");
		let wrapper = this.elements.parent.find(".wrapper");
		if (wrapper.length) {
			wrapper.html(html);
		} else {
			this.elements.parent.append(html);
		}

	}
	animate() {
		$(document).ready(function () {
			$( ".module_name" ).click(function() {
				let parent_box = $(this).closest('.row');
				parent_box.siblings().find('.favourites').slideUp(500,'swing');
				parent_box.find('.favourites').slideToggle(500, 'swing');
			});
		});
	}
}

