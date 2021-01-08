frappe.pages["admin_insights"].on_page_load = function (wrapper) {
  new frappe.views.InsightsFactory().make("admin_insights");
};

frappe.views.InsightsFactory = class InsightsFactory extends (
  frappe.views.Factory
) {
  make(page_name) {
    const assets = [
      "assets/bloomstack_core/js/min/admin_insights.min.js",
      "assets/bloomstack_core/css/admin_insights.css",
    ];
    frappe.call({
      method:
        "bloomstack_core.bloomstack_core.page.admin_insights.admin_insights.get_cubejs_host",
      callback: (r) => {
        frappe.call({
          method:
            "bloomstack_core.bloomstack_core.page.admin_insights.admin_insights.get_all_insights_data",
          callback: ({ message: data }) => {
            frappe.require(assets, () => {
              const sayWhat = new bloomstack_core.admin_insights({
                parent: this.make_page(true, page_name),
                CubeJsHost: r.message.cube_js_host,
                CubeJsSecret: r.message.cube_js_secret,
                cardsData: data,
              });
            });
          },
        });
      },
    });
  }
};
