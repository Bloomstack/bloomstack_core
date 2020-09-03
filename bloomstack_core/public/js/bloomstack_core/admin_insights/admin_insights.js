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
    this.setup_content();
    this.make_body();
  }
  make_body() {
    this.$admin_insights_container = this.$parent.find(".layout-main");
    new Vue({
	  render: h => h(Home),
      data: {
        page: this.page,
      },
    }).$mount("#content");
  }
  setup_header() {
    this.page.set_title(__("Admin Insights"));
  }
  setup_content() {
    var content = document.createElement("div");
    content.setAttribute("id", "content");
    document.getElementsByClassName("container")[0].appendChild(content);
  }
};
