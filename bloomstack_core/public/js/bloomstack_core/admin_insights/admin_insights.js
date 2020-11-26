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
  constructor({ parent, Cube_Js_Host, Cube_Js_Secret }) {
    this.$parent = $(parent);
    this.page = parent.page;
    this.config = { Cube_Js_Host, Cube_Js_Secret }
    this.SetUpHeader();
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
  SetUpHeader() {
    this.page.set_title(__("Admin Insights"));
  }
};
// console.log("hello", bloomstack_core.admin_insights);