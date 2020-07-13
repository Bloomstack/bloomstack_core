import Home from './Home.vue';
import store from "../store/store";
import Paginate from 'vuejs-paginate';


Vue.component('paginate', Paginate)

frappe.provide('bloomstack_core.license_seach');

bloomstack_core.license_seach = class LicenseSearch {
	constructor({ parent }) {
		this.$parent = $(parent);
		this.page = parent.page;
		this.setup_header();
		this.make_body();
	}
	make_body() {
		this.$license_search_container = this.$parent.find('.layout-main');
		new Vue({
			store,
			el: this.$license_search_container[0],
			render: h => h(Home),
			data: {
				'page': this.page
			}
		});
	}
	setup_header() {
		this.page.set_title(__('License Search'));
	}
};
