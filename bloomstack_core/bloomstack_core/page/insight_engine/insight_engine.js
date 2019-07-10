{% include "bloomstack_core/bloomstack_core/page/insight_engine/insight_engine.html" %}

frappe.pages['insight-engine'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Insight Engine',
		single_column: true
	});

	wrapper.insight_engine = new InsightEngine(wrapper);
}


InsightEngine = class InsightEngine {
	constructor(wrapper) {
		this.setup(wrapper);
		const assets = [
			'assets/js/chart.js',
			'assets/bloomstack_core/css/insight_engine.css'
		];

		frappe.require(assets, () => {
			this.make();
		});
	}

	setup(wrapper) {
		let me = this;
		this.elements = {
			parent: $(wrapper).find(".layout-main"),
			refresh_btn: wrapper.page.set_primary_action(__("Refresh All"), () => { me.make() }, "fa fa-refresh"),
		};

		this.elements.no_data = $('<div class="alert alert-warning">' + __("No Data") + '</div>')
			.toggle(false)
			.appendTo(this.elements.parent);
	}

	async make() {
		await this.getData();
		this.renderPage();
		this.renderCharts();
	}

	async getData() {
		let me = this;
		await frappe.call({
			method: "bloomstack_core.bloomstack_core.page.insight_engine.insight_engine.get_insight_engine_dashboards",
			callback: (r) => {
				if (!r.exc && r.message) {
					me.dashboard_data = r.message;
				} else {
					me.elements.no_data.toggle(true);
				}
			}
		});
	}

	getDateRangeAsArray(startDate, stopDate) {
		let dateArray = [];

		// Default the dashboard input dates to a week
		startDate = moment(startDate || moment().subtract(7, 'days'));
		stopDate = moment(stopDate || moment().subtract(1, 'day'));

		while (startDate <= stopDate) {
			dateArray.push(moment(startDate).format('MMM D'))
			startDate = moment(startDate).add(1, 'day');
		}

		return dateArray;
	}

	renderPage() {
		let html = frappe.render_template("insight_engine", this.dashboard_data)
		this.elements.parent.html(html);
	}

	renderCharts() {
		const opacity = 0.6;
		const colors = {
			hex: [
				// no opacity
				'#F58767',
				'#505362',
				'#69829E',
				'#80BD9E',
				'#ADBD38',
				'#598233',
				// hack to repeat colors
				'#F58767',
				'#505362',
				'#69829E',
				'#80BD9E',
				'#ADBD38',
				'#598233'
			],
			rgba: [
				// applied opacity
				`rgba(245, 135, 103, ${opacity})`,
				`rgba(80, 83, 98, ${opacity})`,
				`rgba(105, 130, 158, ${opacity})`,
				`rgba(128, 189, 158, ${opacity})`,
				`rgba(173, 189, 56, ${opacity})`,
				`rgba(89, 130, 5, ${opacity})`,
				// hack to repeat colors
				`rgba(245, 135, 103, ${opacity})`,
				`rgba(80, 83, 98, ${opacity})`,
				`rgba(105, 130, 158, ${opacity})`,
				`rgba(128, 189, 158, ${opacity})`,
				`rgba(173, 189, 56, ${opacity})`,
				`rgba(89, 130, 5, ${opacity})`
			]
		}

		// Top product trends in the last week
		let datasets = [];
		Object.keys(this.dashboard_data.top_products_by_time).forEach((item, i) => {
			datasets.push({
				label: item,
				backgroundColor: colors.rgba[i],
				borderColor: colors.hex[i],
				borderWidth: 1.5,
				fill: false,
				data: this.dashboard_data.top_products_by_time[item]
			})
		});

		new Chart($(".chart-graphics"), {
			type: 'line',
			data: {
				labels: this.getDateRangeAsArray(),
				datasets: datasets
			},
			options: {
				legend: { position: 'bottom' },
				layout: { padding: 30 },
				scales: {
					xAxes: [{
						gridLines: { display: false }
					}],
					yAxes: [{
						gridLines: { display: false },
						ticks: {
							callback(value, index, values) {
								return format_currency(value, null, 0);
							}
						}
					}]
				},
				tooltips: {
					callbacks: {
						label(tooltipItem, data) {
							return format_currency(tooltipItem.value);
						}
					}
				}
			}
		});

		// Sales by territories
		new Chart($(".category-product-info .donut-chart .graphics"), {
			type: 'doughnut',
			data: {
				labels: this.dashboard_data.top_territories_by_revenue.map(elem => elem.territory),
				datasets: [{
					data: this.dashboard_data.top_territories_by_revenue.map(elem => elem.grand_total),
					backgroundColor: colors.rgba,
					borderColor: colors.hex,
					borderWidth: 1.5
				}]
			},
			options: {
				layout: { padding: 30 },
				legend: { position: 'left' },
				tooltips: {
					callbacks: {
						label(tooltipItem, data) {
							return format_currency(data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]);
						}
					}
				}
			}
		});

		// Top products
		this.dashboard_data.top_products_by_revenue.map((data, i) => {
			let row = `
				<tr>
					<td> ${ (i+1) } </td>
					<td> ${ data.item } </td>
					<td> ${ format_currency(data.revenue) } </td>
					<td> ${ data.volume } </td>
				</tr>
			`;
			$('.table-data tbody').append(row);
		});

		// Top sales partners
		new Chart($(".bar-data .graphics"), {
			type: 'horizontalBar',
			data: {
				labels: this.dashboard_data.top_sales_partners_by_revenue.map(elem => elem.sales_partner),
				datasets: [{
					data: this.dashboard_data.top_sales_partners_by_revenue.map(elem => elem.grand_total),
					backgroundColor: colors.rgba,
					borderColor: colors.hex,
					borderWidth: 1.5
				}]
			},
			options: {
				legend: { display: false },
				layout: { padding: 30 },
				scales: {
					xAxes: [{
						gridLines: { display: false },
						barThickness: 30,
						ticks: {
							callback(value, index, values) {
								return format_currency(value, null, 0);
							}
						}
					}],
					yAxes: [{
						gridLines: { display: false },
						ticks: { beginAtZero: true },
					}]
				},
				tooltips: {
					callbacks: {
						label(tooltipItem, data) {
							return format_currency(tooltipItem.value);
						}
					}
				}
			}
		});

		// 2nd donut
		new Chart($(".sales-partner-info .donut-chart .graphics"), {
			type: 'doughnut',
			data: {
				labels: ['overdue_invoices', 'unpaid_invoices'],
				datasets: [{
					data: [this.dashboard_data.overdue_invoices, this.dashboard_data.unpaid_invoices],
					backgroundColor: colors.rgba,
					borderColor: colors.hex,
					borderWidth: 1.5
				}]
			},
			options: {
				layout: { padding: 30 },
				legend: { position: 'left' },
				tooltips: {
					callbacks: {
						label(tooltipItem, data) {
							return format_currency(data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]);
						}
					}
				}
			}
		});

		// Top customers
		new Chart($(".graphical-distribution .graphics"), {
			type: 'horizontalBar',
			data: {
				labels: this.dashboard_data.top_customers_by_revenue.map(elem => elem.customer),
				datasets: [{
					data: this.dashboard_data.top_customers_by_revenue.map(elem => elem.grand_total),
					backgroundColor: colors.rgba,
					borderColor: colors.hex,
					borderWidth: 1.5
				}]
			},
			options: {
				legend: { display: false },
				layout: { padding: 30 },
				scales: {
					xAxes: [{
						gridLines: { display: false },
						barThickness: 30,
						ticks: {
							beginAtZero: true,
							callback(value, index, values) {
								return format_currency(value, null, 0);
							}
						}
					}],
					yAxes: [{
						gridLines: { display: false }
					}]
				},
				tooltips: {
					callbacks: {
						label(tooltipItem, data) {
							return format_currency(tooltipItem.value);
						}
					}
				}
			}
		});
	}
}
