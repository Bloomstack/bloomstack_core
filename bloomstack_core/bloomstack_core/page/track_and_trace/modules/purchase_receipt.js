/* global frappe, bloomstack */

bloomstack.track_and_trace.modules.add("Purchase Receipt", {
    fields: [
        { field: "work_order", label: "Work Order" },
        { field: "posting_date", label: "Posting Date", fieldtype: "Date" }
    ],

    icon: "fa fa-book"
});

bloomstack.track_and_trace.modules.add("Purchase Receipt Item", {
    fields: [
        { field: "item_name", label: "Item Name" },
        { field: "qty", label: "Qty" },
        { field: "stock_uom", label: "UOM" },
        { field: "rate", label: "Rate", fieldtype: "Currency" },
        { field: "amount", label: "Amount", fieldtype: "Currency" },
        { field: "purchase_order", label: "Purchase Order" }
    ],

    icon: "fa fa-file-text-o",
    
    has_route: false,

    format(data) {
        let item = data.data;
        data.title = `${item.item_code}: ${item.item_name}`;

        return data;
    }

});