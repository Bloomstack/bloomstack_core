frappe.ui.form.on('Purchase Order', {
	reverse_calculate: function(frm) {
		let data = [];
		for (let row of frm.doc.items) {
			data.push({
				"docname": row.name,
				"item_code": row.item_code,
				"item_name": row.item_name,
				"qty": row.qty,
				"rate": row.rate,
				"amount": row.amount
			})
		}

		const dialog = new frappe.ui.Dialog({
			title: __("Set Amount for items"),
			fields: [
				{
					label: __("Items"),
					fieldname: "items",
					fieldtype: "Table",
					cannot_add_rows: true,
					data: data,
					in_place_edit: true,
					get_data: () => {
						return this.data;
					},
					fields: [
						{
							fieldtype: 'Data',
							fieldname: "docname",
							hidden: 1
						},
						{
							label: __("Item Code"),
							fieldtype: 'Link',
							fieldname: "item_code",
							options: "Item",
							read_only: 1,
							in_list_view: 1
						},
						{
							label: __("Item Name"),
							fieldtype: 'Data',
							fieldname: "item_name",
							read_only: 1,
							in_list_view: 1
						},
						{
							label: __("Qty"),
							fieldtype: 'Data',
							fieldname: 'qty',
							read_only: 1,
							in_list_view: 1
						},
						{
							label: __("Rate"),
							fieldtype: 'Data',
							fieldname: 'rate',
							read_only: 1,
							in_list_view: 1
						},
						{
							label: __("Amount"),
							fieldtype: 'Data',
							fieldname: 'amount',
							in_list_view: 1
						}
					],
				}
			],
			primary_action: function () {
				const values = dialog.get_values().items;
				values.forEach(d => {
					let rate = d.amount / d.qty;
					frappe.model.set_value("Purchase Order Item", d.docname, "rate", rate);
				});

				dialog.hide();
				frappe.show_alert({
					indicator: 'green',
					message: __("The amount have been successfully set")
				});
			},
			primary_action_label: __('Set Amount')
		})
		dialog.show();
	}
})