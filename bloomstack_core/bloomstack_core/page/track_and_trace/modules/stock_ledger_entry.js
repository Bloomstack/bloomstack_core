/* global frappe, bloomstack */

bloomstack.track_and_trace.modules.add("Stock Ledger Entry", {
	fields: [
		{ field: "actual_qty", label: "Qty" },
		{ field: "stock_uom", label: "UOM" },
		{ field: "warehouse", label: "Warehouse" },
		{ field: "item_code", label: "Item" }
	],

	icon: "fa fa-pencil-square-o",

	has_route: false,

	format(data) {
		let entry = data.data;

		if ( entry.voucher_no && entry.voucher_type ) {
			let qty_arrow = (entry.actual_qty > 0)?"fa-arrow-up positive":(entry.actual_qty < 0)?"fa-arrow-down negative":"";
			let from_to_lbl = (entry.actual_qty > 0)?"FROM":(entry.actual_qty < 0)?"TO":"";
			data.title = `<i  class="fa ${qty_arrow}"/>${from_to_lbl} ${entry.voucher_type}: ${entry.voucher_no}`;
			
			data.children.push({
				query: true,
				dt: entry.voucher_type,
				dn: entry.voucher_no,
				search_dt: data.search_dt,
				search_dn: data.search_dn
			});

		}

		return bloomstack.get_value("Item", "name", { item_code: entry.item_code })
			.then((v) => {
				entry.item_name = `<a data-route-dt="Item" data-route-dn="${v.name}">${entry.item_code}</a>`;

				return data;
			})
	}

});
