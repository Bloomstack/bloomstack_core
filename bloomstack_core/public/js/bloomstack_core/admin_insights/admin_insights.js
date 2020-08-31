import Vue from 'vue/dist/vue.js';
import { Laue } from 'laue';
import Home from './Home.vue';

Vue.use(Laue);

frappe.provide('bloomstack_core.admin_insights');

bloomstack_core.admin_insights = class AdminInsights {
	constructor({ parent }) {
		this.$parent = $(parent);
		this.page = parent.page;
		this.setup_header();
		this.make_body();
	}
	make_body() {
		this.$admin_insights_container = this.$parent.find('.layout-main');
		new Vue({
			el: this.$admin_insights_container[0],
			render: h => h(Home),
			data: {
				'page': this.page
			}
		}).$mount("#home");
	}
	setup_header() {
		this.page.set_title(__('Admin Insightss'));
	}
};