import Vue from "vue/dist/vue.js";
import { Laue } from "laue";
import Home from "./Home.vue";
import VueGoogleCharts from "vue-google-charts";

Vue.use(VueGoogleCharts);
Vue.use(Laue);
Vue.config.productionTip = false;
Vue.config.errorHandler = function (err) {
  console.log("Error is..........", err.message); // "Oops"
};

frappe.provide("bloomstack_core.admin_insights");
bloomstack_core.admin_insights = class AdminInsights {
  constructor({ parent, CubeJsHost, CubeJsSecret }) {
    this.$parent = $(parent);
    this.page = parent.page;
    this.config = { CubeJsHost, CubeJsSecret };
    this.setUpHeader();
    this.make_body();
  }
  make_body() {
    new Vue({
      render: (h) => h(Home, {
        props: {
          config: this.config
        }
      }),
      data: {
        page: this.page,
      },
    }).$mount(".layout-main")[0];
  }
  setUpHeader() {
    this.page.set_title(__("Admin Insights"));
  }
};
// console.log("hello", bloomstack_core.admin_insights);