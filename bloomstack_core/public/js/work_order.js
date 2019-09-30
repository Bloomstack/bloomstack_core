frappe.ui.form.on("Work Order", {
	setup: (frm) => {
		frappe.meta.docfield_map["Work Order Operation"].operation.formatter =
			function (value, df, options, doc) {
				if (!value) {
					return '';
				}

				let label;
				if (frappe.form.link_formatters[df.options]) {
					label = frappe.form.link_formatters[df.options](value, doc);
				} else {
					label = value;
				}

				let color;
				if (!doc.completed_qty) {
					color = "red";
				} else if (doc.completed_qty < frm.doc.qty) {
					color = "orange";
				} else if (doc.completed_qty == frm.doc.qty) {
					color = "green";
				}

				const escaped_name = encodeURIComponent(value);

				return repl('<a class="indicator %(color)s" href="#Form/%(doctype)s/%(name)s">%(label)s</a>', {
					color: color,
					doctype: df.options,
					name: escaped_name,
					label: label
				});
			};
	}
});