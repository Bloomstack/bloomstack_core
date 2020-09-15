import Vue from "vue/dist/vue.js";
import { Laue } from "laue";
import Home from "./Home.vue";

Vue.use(Laue);
Vue.config.productionTip = false;
Vue.config.errorHandler = function (err) {
	console.log("Error is..........", err.message); // "Oops"
  };
frappe.provide("bloomstack_core.admin_insights");

bloomstack_core.admin_insights = class AdminInsights {
  constructor({ parent }) {
    this.$parent = $(parent);
    this.page = parent.page;
    this.setup_header();
    this.make_body();
  }
  make_body() {
    new Vue({
	  render: h => h(Home),
      data: {
        page: this.page,
      },
    }).$mount("#content-row");
  }
  setup_header() {
    this.page.set_title(__("Admin Insights"));
  }
};
