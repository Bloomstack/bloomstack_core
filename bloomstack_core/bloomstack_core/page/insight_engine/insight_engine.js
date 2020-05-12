{% include "bloomstack_core/bloomstack_core/page/insight_engine/insight_engine.html" %}

frappe.pages['insight-engine'].on_page_load = function(wrapper) {
	wrapper.insight_engine = new InsightEngine(wrapper);
}


class InsightEngine {
	constructor(parent) {
		frappe.ui.make_app_page({
			parent: parent,
			title: 'Dashboard',
			single_column: true
		});

		this.setup(parent);
		const assets = [
			'assets/js/chart.js',
			'assets/bloomstack_core/css/insight_engine.css'
		];

		frappe.require(assets, () => {
			this.make();
		});
	}

	setup(parent) {
		let me = this;

		// set default start date to last year start
		let startDateControl = parent.page.add_date("Start Date", moment().subtract(1, "year").startOf("year").format())
			.change(() => { me.make() })
		let endDateControl = parent.page.add_date("End Date", frappe.datetime.now_datetime())
			.change(() => { me.make() })

		this.elements = {
			page: parent.page,
			start_date: startDateControl,
			end_date: endDateControl,
			parent: $(parent).find(".layout-main"),
			refresh_btn: parent.page.set_primary_action(__("Refresh All"), () => { me.make() }, "fa fa-refresh"),
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
			args: {
				start_date: me.elements.start_date.val(),
				end_date: me.elements.end_date.val(),
			},
			callback: (r) => {
				if (!r.exc && r.message) {
					me.dashboardData = r.message;
					me.dashboardData.startDate = me.elements.start_date.val();
					me.dashboardData.endDate = me.elements.end_date.val();
				} else {
					me.elements.no_data.toggle(true);
				}
			}
		});
	}

	getDateRangeAsArray(startDate, endDate, period) {
		let dateArray = [];

		// Default the dashboard input dates to the selected date range
		startDate = moment(startDate || this.dashboardData.startDate);
		endDate = moment(endDate || this.dashboardData.endDate);

		let dateFormat;
		if (period === "year") {
			dateFormat = "Y";
		} else if (period === "month") {
			dateFormat = startDate.year() != endDate.year() ? 'MMM Y' : 'MMM';
		} else {
			dateFormat = startDate.year() != endDate.year() ? 'MMM D Y' : 'MMM D';
		}

		while (startDate <= endDate) {
			dateArray.push(startDate.format(dateFormat));
			startDate = startDate.add(1, period);
		}

		return dateArray;
	}

	renderPage() {
		let html = frappe.render_template("insight_engine", this.dashboardData);
		let wrapper = this.elements.parent.find(".wrapper");

		if (wrapper.length) {
			wrapper.html(html);
		} else {
			this.elements.parent.append(html);
		}
	}

	renderCharts() {
		// set global datalabel defaults
		Chart.defaults.global.plugins.datalabels.anchor = 'end';
		Chart.defaults.global.plugins.datalabels.align = 'end';

		const currentYear = moment().year();
		const lastYear = moment().subtract(1, "year").year();
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

		// split list of sales revenue by year
		let currentYearRevenue = this.dashboardData.total_sales_by_month.filter(elem => elem.year == currentYear).map(elem => elem.revenue)
		let lastYearRevenue = this.dashboardData.total_sales_by_month.filter(elem => elem.year == lastYear).map(elem => elem.revenue)

		let currentYearCumulativeRevenue = currentYearRevenue.reduce((prev, next, i) => [...prev, next + (prev[i - 1] || 0)], [])
		let lastYearCumulativeRevenue = lastYearRevenue.reduce((prev, next, i) => [...prev, next + (prev[i - 1] || 0)], [])

		// MTD revenue vs last year
		new Chart($(".total-revenue .left-chart .graphics"), {
			type: 'line',
			data: {
				labels: this.getDateRangeAsArray(frappe.datetime.year_start(), frappe.datetime.year_end(), "month"),
				datasets: [
					{
						label: currentYear,
						data: currentYearRevenue,
						backgroundColor: colors.rgba[0],
						borderColor: colors.hex[0],
						borderWidth: 1.5,
						fill: false
					},
					{
						label: lastYear,
						data: lastYearRevenue,
						backgroundColor: colors.rgba[1],
						borderColor: colors.hex[1],
						borderWidth: 1.5,
						fill: false
					}
				]
			},
			options: {
				legend: {
					display: true,
					position: 'bottom'
				},
				layout: { padding: 30 },
				scales: {
					xAxes: [{
						type: 'category',
						time: { minUnit: "month" },
						gridLines: { display: false },
						distribution: 'series'
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
				plugins: {
					datalabels: {
						display: false
					}
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

		// YTD revenue vs last year
		new Chart($(".total-revenue .right-chart .graphics"), {
			type: 'line',
			data: {
				labels: this.getDateRangeAsArray(frappe.datetime.year_start(), frappe.datetime.year_end(), "month"),
				datasets: [
					{
						label: currentYear,
						data: currentYearCumulativeRevenue,
						backgroundColor: colors.rgba[0],
						borderColor: colors.hex[0],
						borderWidth: 1.5,
						fill: false
					},
					{
						label: lastYear,
						data: lastYearCumulativeRevenue,
						backgroundColor: colors.rgba[1],
						borderColor: colors.hex[1],
						borderWidth: 1.5,
						fill: false
					}
				]
			},
			options: {
				legend: {
					display: true,
					position: 'bottom'
				},
				layout: { padding: 30 },
				scales: {
					xAxes: [{
						type: 'category',
						time: { minUnit: "month" },
						gridLines: { display: false },
						distribution: 'series'
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
				plugins: {
					datalabels: {
						display: false
					}
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

		// split list of upsell revenue by year
		let currentYearUpsellRevenue = this.dashboardData.total_upsell_sales_by_month.filter(elem => elem.year == currentYear).map(elem => elem.revenue)
		let lastYearUpsellRevenue = this.dashboardData.total_upsell_sales_by_month.filter(elem => elem.year == lastYear).map(elem => elem.revenue)

		let currentYearCumulativeUpsellRevenue = currentYearUpsellRevenue.reduce((prev, next, i) => [...prev, next + (prev[i - 1] || 0)], [])
		let lastYearCumulativeUpsellRevenue = lastYearUpsellRevenue.reduce((prev, next, i) => [...prev, next + (prev[i - 1] || 0)], [])

		// MTD Sales Partner upsell vs last year
		new Chart($(".total-upsell-revenue .left-chart .graphics"), {
			type: 'line',
			data: {
				labels: this.getDateRangeAsArray(frappe.datetime.year_start(), frappe.datetime.year_end(), "month"),
				datasets: [
					{
						label: currentYear,
						data: currentYearUpsellRevenue,
						backgroundColor: colors.rgba[0],
						borderColor: colors.hex[0],
						borderWidth: 1.5,
						fill: false
					},
					{
						label: lastYear,
						data: lastYearUpsellRevenue,
						backgroundColor: colors.rgba[1],
						borderColor: colors.hex[1],
						borderWidth: 1.5,
						fill: false
					}
				]
			},
			options: {
				legend: {
					display: true,
					position: 'bottom'
				},
				layout: { padding: 30 },
				scales: {
					xAxes: [{
						type: 'category',
						time: { minUnit: "month" },
						gridLines: { display: false },
						distribution: 'series'
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
				plugins: {
					datalabels: {
						display: false
					}
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

		// YTD Sales Partner upsell vs last year
		new Chart($(".total-upsell-revenue .right-chart .graphics"), {
			type: 'line',
			data: {
				labels: this.getDateRangeAsArray(frappe.datetime.year_start(), frappe.datetime.year_end(), "month"),
				datasets: [
					{
						label: currentYear,
						data: currentYearCumulativeUpsellRevenue,
						backgroundColor: colors.rgba[0],
						borderColor: colors.hex[0],
						borderWidth: 1.5,
						fill: false
					},
					{
						label: lastYear,
						data: lastYearCumulativeUpsellRevenue,
						backgroundColor: colors.rgba[1],
						borderColor: colors.hex[1],
						borderWidth: 1.5,
						fill: false
					}
				]
			},
			options: {
				legend: {
					display: true,
					position: 'bottom'
				},
				layout: { padding: 30 },
				scales: {
					xAxes: [{
						type: 'category',
						time: { minUnit: "month" },
						gridLines: { display: false },
						distribution: 'series'
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
				plugins: {
					datalabels: {
						display: false
					}
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

		// Daily sales trends in the last 30 days
		new Chart($(".chart-container .chart-graphics"), {
			type: 'line',
			data: {
				labels: this.getDateRangeAsArray(this.dashboardData.startDate, this.dashboardData.endDate, "week"),
				datasets: [{
					data: this.dashboardData.total_sales_by_week.map(elem => elem.revenue),
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
						type: 'time',
						time: { minUnit: "month" },
						gridLines: { display: false },
						distribution: 'series'
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
				plugins: {
					datalabels: {
						display: false
					}
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
		new Chart($(".category-product-info .left-chart .graphics"), {
			type: 'doughnut',
			data: {
				labels: this.dashboardData.top_territories_by_revenue.map(elem => elem.territory),
				datasets: [{
					data: this.dashboardData.top_territories_by_revenue.map(elem => elem.grand_total),
					backgroundColor: colors.rgba,
					borderColor: colors.hex,
					borderWidth: 1.5
				}]
			},
			options: {
				layout: { padding: 30 },
				legend: { position: 'left' },
				plugins: {
					datalabels: {
						display: false
					}
				},
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
		new Chart($(".category-product-info .right-chart .graphics"), {
			type: 'horizontalBar',
			data: {
				labels: this.dashboardData.top_products_by_revenue.map(elem => elem.item),
				datasets: [{
					data: this.dashboardData.top_products_by_revenue.map(elem => elem.revenue),
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
				plugins: {
					datalabels: {
						display: false
					}
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
		new Chart($(".sales-partner-info .left-chart .graphics"), {
			type: 'horizontalBar',
			data: {
				labels: this.dashboardData.top_sales_partners_by_revenue.map(elem => elem.sales_partner),
				datasets: [{
					data: this.dashboardData.top_sales_partners_by_revenue.map(elem => elem.grand_total),
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
				plugins: {
					datalabels: {
						display: false
					}
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

		// All invoice breakdown by status
		new Chart($(".sales-partner-info .right-chart .graphics"), {
			type: 'doughnut',
			data: {
				labels: ['Paid', 'Unpaid', 'Overdue', 'Returned', 'Credit Issued'],
				datasets: [{
					data: [
						this.dashboardData.paid_invoices,
						this.dashboardData.unpaid_invoices,
						this.dashboardData.overdue_invoices,
						this.dashboardData.returned_invoices,
						this.dashboardData.credit_invoices
					],
					backgroundColor: colors.rgba,
					borderColor: colors.hex,
					borderWidth: 1.5
				}]
			},
			options: {
				layout: { padding: 30 },
				legend: { position: 'left' },
				plugins: {
					datalabels: {
						display: false
					}
				},
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
		new Chart($(".graphical-distribution .left-chart .graphics"), {
			type: 'bar',
			data: {
				labels: this.dashboardData.top_customers_by_revenue.map(elem => elem.customer),
				datasets: [{
					data: this.dashboardData.top_customers_by_revenue.map(elem => elem.grand_total),
					backgroundColor: colors.rgba[2],
					borderColor: colors.hex[2],
					borderWidth: 1.5
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
						barThickness: 30,
						ticks: {
							beginAtZero: true,
							callback(value, index, values) {
								return format_currency(value, null, 0);
							}
						}
					}]
				},
				plugins: {
					datalabels: {
						display: false
					}
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
		new Chart($(".graphical-distribution .right-chart .graphics"), {
			type: 'bar',
			data: {
				labels: this.dashboardData.top_customer_groups_by_revenue.map(elem => elem.customer_group),
				datasets: [{
					data: this.dashboardData.top_customer_groups_by_revenue.map(elem => elem.grand_total),
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
				plugins: {
					datalabels: {
						display: false
					}
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
		// new Chart($(".customer-distribution .left-chart .graphics"), {
		// 	type: 'bar',
		// 	data: {
		// 		labels: this.dashboardData.total_customers_by_month.map(elem => elem.month),
		// 		datasets: [
		// 			{
		// 				label: "New Customers",
		// 				data: this.dashboardData.new_customers_by_month.map(elem => elem.count),
		// 				backgroundColor: colors.rgba[2],
		// 				borderColor: colors.hex[2],
		// 				borderWidth: 1.5
		// 			},
		// 			{
		// 				label: "Total Customers",
		// 				data: this.dashboardData.total_customers_by_month.map(elem => elem.count),
		// 				backgroundColor: colors.rgba[3],
		// 				borderColor: colors.hex[3],
		// 				borderWidth: 1.5
		// 			}
		// 		]
		// 	},
		// 	options: {
		// 		legend: { position: 'bottom' },
		// 		layout: { padding: 30 },
		// 		scales: {
		// 			xAxes: [{
		// 				gridLines: { display: false }
		// 			}],
		// 			yAxes: [{
		// 				gridLines: { display: false },
		// 				barThickness: 30,
		// 				ticks: {
		// 					beginAtZero: true
		// 				}
		// 			}]
		// 		}
		// 	}
		// });

		// New customer vs total customer sales by month
		// new Chart($(".customer-distribution .right-chart .graphics"), {
		// 	type: 'bar',
		// 	data: {
		// 		labels: this.dashboardData.total_customer_sales_by_month.map(elem => elem.month),
		// 		datasets: [
		// 			{
		// 				label: "New Customers",
		// 				data: this.dashboardData.new_customer_sales_by_month.map(elem => elem.revenue),
		// 				backgroundColor: colors.rgba[2],
		// 				borderColor: colors.hex[2],
		// 				borderWidth: 1.5
		// 			},
		// 			{
		// 				label: "Total Customers",
		// 				data: this.dashboardData.total_customer_sales_by_month.map(elem => elem.revenue),
		// 				backgroundColor: colors.rgba[3],
		// 				borderColor: colors.hex[3],
		// 				borderWidth: 1.5
		// 			}
		// 		]
		// 	},
		// 	options: {
		// 		legend: { position: 'bottom' },
		// 		layout: { padding: 30 },
		// 		scales: {
		// 			xAxes: [{
		// 				gridLines: { display: false }
		// 			}],
		// 			yAxes: [{
		// 				gridLines: { display: false },
		// 				barThickness: 30,
		// 				ticks: {
		// 					beginAtZero: true,
		// 					callback(value, index, values) {
		// 						return format_currency(value, null, 0);
		// 					}
		// 				}
		// 			}]
		// 		},
		// 		plugins: {
		// 			datalabels: {
		// 				formatter(value, context) {
		// 					return format_currency(value, null, 0);
		// 				}
		// 			}
		// 		},
		// 		tooltips: {
		// 			callbacks: {
		// 				label(tooltipItem, data) {
		// 					return format_currency(tooltipItem.value);
		// 				}
		// 			}
		// 		}
		// 	}
		// });
	}
}
