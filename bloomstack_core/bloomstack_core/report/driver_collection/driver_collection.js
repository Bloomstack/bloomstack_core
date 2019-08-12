// Copyright (c) 2016, Neil Lasrado and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Driver Collection"] = {
	"filters": [
		{
			"fieldname": "driver",
			"label": __("Driver"),
			"fieldtype": "Link",
			"options": "Driver",
			"get_query": () => {
				return { filters: { "status": "Active" } }
			}
		},
		{
			"fieldname": "date_range",
			"label": __("Delivery Date Range"),
			"fieldtype": "DateRange",
			"default": [frappe.datetime.get_today(), frappe.datetime.get_today()],
			"reqd": 1
		},
		{
			"fieldname": "period",
			"label": __("Delivery Period"),
			"fieldtype": "Select",
			"options": [
				{ "value": "Today", "label": __("Today") },
				{ "value": "Last 7 Days", "label": __("Last 7 Days") },
				{ "value": "Month to Date", "label": __("Month to Date") },
				{ "value": "Last 30 Days", "label": __("Last 30 Days") },
				{ "value": "Last 90 Days", "label": __("Last 90 Days") },
				{ "value": "Year to Date", "label": __("Year to Date") },
				{ "value": "Last 365 Days", "label": __("Last 365 Days") }
			],
			"default": "Today",
			on_change: () => {
				let period = frappe.query_report.get_filter_value('period');
				const now_date = frappe.datetime.nowdate()

				decrement = {
					"Today": 0,
					"Last 7 Days": 7,
					"Month to Date": frappe.datetime.get_day_diff(now_date, frappe.datetime.month_start()),
					"Last 30 Days": 30,
					"Last 90 Days": 90,
					"Year to Date": frappe.datetime.get_day_diff(now_date, frappe.datetime.year_start()),
					"Last 365 Days": 365
				}[period]

				frappe.query_report.set_filter_value('date_range', [
					frappe.datetime.add_days(now_date, -decrement),
					now_date
				]);
			}
		},
		{
			"fieldname": "show_individual_stops",
			"label": __("Show Individual Stops"),
			"fieldtype": "Check"
		},
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (["expected_amount", "total_payment"].includes(column.fieldname) && data) {
			// compare values with precision of 2
			if (data.expected_amount.toFixed(2) > data.total_payment.toFixed(2)) {
				value = "<span style='color:red'>" + value + "</span>";
			} else {
				value = "<span style='color:green'>" + value + "</span>";
			}
		}

		return value;
	},
	get_chart_data: (columns, result) => {
		let results = {}
		for (let row of result) {
			// Since the total row is last, break loop
			if (["Total", "'Total'"].includes(row[0])) { break; };

			let pending = row.total_payment < row.expected_amount ? row.expected_amount - row.total_payment : 0;

			results[row.driver] = results[row.driver] || {
				unprocessed: 0,
				processed: 0,
				pending: 0
			}
			results[row.driver].unprocessed += row.payment_received;
			results[row.driver].processed += row.payment_processed;
			results[row.driver].pending += pending;
		}

		const labels = Object.keys(results);
		const values = Object.values(results);

		return {
			data: {
				labels: labels,
				datasets: [
					{
						name: "Unprocessed",
						values: values.map(row => row.unprocessed),
						chartType: "bar"
					},
					{
						name: "Processed",
						values: values.map(row => row.processed),
						chartType: "bar"
					},
					{
						name: "Pending",
						values: values.map(row => row.pending),
						chartType: "bar"
					}
				]
			},
			type: "axis-mixed",
			colors: ["yellow", "green", "red"],
			barOptions: {
				spaceRatio: 0.6,
				stacked: 1
			},
			tooltipOptions: {
				formatTooltipY: d => format_currency(d),
			}
		}
	}
}