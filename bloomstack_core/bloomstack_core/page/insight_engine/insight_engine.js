{% include "bloomstack_core/bloomstack_core/page/insight_engine/insight_engine.html" %}

frappe.pages['insight-engine'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Dashboard',
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

		// Weekly sales trends in the last week
		let startDate = moment().subtract(30, 'days');
		let stopDate = moment().subtract(1, 'day');

		new Chart($(".chart-graphics"), {
			type: 'line',
			data: {
				labels: this.getDateRangeAsArray(startDate, stopDate),
				datasets: [{
					data: this.dashboard_data.total_sales_by_day.map(elem => elem.revenue),
					backgroundColor: colors.rgba[0],
					borderColor: colors.hex[0],
					borderWidth: 1.5,
					fill: false
				}]
			},
			options: {
				legend: { display: false },
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
		new Chart($(".table-data .graphics"), {
			type: 'horizontalBar',
			data: {
				labels: this.dashboard_data.top_products_by_revenue.map(elem => elem.item),
				datasets: [{
					data: this.dashboard_data.top_products_by_revenue.map(elem => elem.revenue),
					backgroundColor: colors.rgba[3],
					borderColor: colors.hex[3],
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

		// 2nd donut
		new Chart($(".sales-partner-info .donut-chart .graphics"), {
			type: 'doughnut',
			data: {
				labels: ['Paid', 'Unpaid', 'Overdue', 'Returned', 'Credit Issued'],
				datasets: [{
					data: [
						this.dashboard_data.paid_invoices,
						this.dashboard_data.unpaid_invoices,
						this.dashboard_data.overdue_invoices,
						this.dashboard_data.returned_invoices,
						this.dashboard_data.credit_invoices
					],
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
		new Chart($(".graphical-distribution .bar-data .graphics"), {
			type: 'horizontalBar',
			data: {
				labels: this.dashboard_data.top_customers_by_revenue.map(elem => elem.customer),
				datasets: [{
					data: this.dashboard_data.top_customers_by_revenue.map(elem => elem.grand_total),
					backgroundColor: colors.rgba[3],
					borderColor: colors.hex[3],
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

		// Top sales by customer groups
		new Chart($(".graphical-distribution .donut-chart .graphics"), {
			type: 'horizontalBar',
			data: {
				labels: this.dashboard_data.top_customer_groups_by_revenue.map(elem => elem.customer_group),
				datasets: [{
					data: this.dashboard_data.top_customer_groups_by_revenue.map(elem => elem.grand_total),
					backgroundColor: colors.rgba[3],
					borderColor: colors.hex[3],
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

		// New customer vs total customer count by month
		new Chart($(".customer-distribution .count-data .graphics"), {
			type: 'bar',
			data: {
				labels: this.dashboard_data.total_customers_by_month.map(elem => elem.month),
				datasets: [
					{
						label: "New Customers",
						data: this.dashboard_data.new_customers_by_month.map(elem => elem.count),
						backgroundColor: colors.rgba[2],
						borderColor: colors.hex[2],
						borderWidth: 1.5
					},
					{
						label: "Total Customers",
						data: this.dashboard_data.total_customers_by_month.map(elem => elem.count),
						backgroundColor: colors.rgba[3],
						borderColor: colors.hex[3],
						borderWidth: 1.5
					}
				]
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
						barThickness: 30,
						ticks: {
							beginAtZero: true
						}
					}]
				}
			}
		});

		// New customer vs total customer sales by month
		new Chart($(".customer-distribution .sales-data .graphics"), {
			type: 'bar',
			data: {
				labels: this.dashboard_data.total_customer_sales_by_month.map(elem => elem.month),
				datasets: [
					{
						label: "New Customers",
						data: this.dashboard_data.new_customer_sales_by_month.map(elem => elem.revenue),
						backgroundColor: colors.rgba[2],
						borderColor: colors.hex[2],
						borderWidth: 1.5
					},
					{
						label: "Total Customers",
						data: this.dashboard_data.total_customer_sales_by_month.map(elem => elem.revenue),
						backgroundColor: colors.rgba[3],
						borderColor: colors.hex[3],
						borderWidth: 1.5
					}
				]
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
						barThickness: 30,
						ticks: {
							beginAtZero: true,
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
	}
}
