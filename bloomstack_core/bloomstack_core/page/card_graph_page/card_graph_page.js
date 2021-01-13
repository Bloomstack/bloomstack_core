frappe.pages["card-graph-page"].on_page_load = function (wrapper) {
	new CardGraphPage(wrapper);
};

CardGraphPage = Class.extend({
	init: function (wrapper) {
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: "Card-Graph Page",
			single_column: true,
		});
		const assets = [
			"assets/bloomstack_core/css/card_graph_page.css"
		];
		frappe.require(assets, () => {
			this.make();
		});
	},
	make: function () {
		$(frappe.render_template("card_graph_page", this)).appendTo(this.page.main);
	}
});

function createQuery() {
	let types = $("#selectOption").find(":selected")[0].text;
	let data_object = $("textarea#cubeJsQuery").val();
	console.log(types, data_object);
	frappe.call({
		method: "bloomstack_core.bloomstack_core.page.admin_insights.admin_insights.create_admin_insights",
		args: {
			types,
			data_object
		},
		callback: (r) => {
			alert(r.message);
		}
	})
}
