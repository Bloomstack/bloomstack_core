/* global frappe, bloomstack */

bloomstack.track_and_trace.modules.add("Serial No", {
    fields: [
        { field: "item_code", label: "Item Code"},
        { field: "item_name", label: "Item Name"},
        { field: "warehouse", label: "Warehouse"}
    ],

    icon: "fa fa-barcode",

    query(dt, dn, data) {
        return bloomstack.track_and_trace.modules
            .default_query(dt, dn, data, this)
            .then((result) => {
                let children = [];
                let serial = result.data;
                if ( serial.purchase_document_type ) {
                    children.push({
                        query: true,
                        search_dt: result.search_dt,
                        search_dn: result.search_dn,
                        dt: serial.purchase_document_type,
                        dn: serial.purchase_document_no
                    })
                }
                result.children = result.children.concat(children);
                return result;
            });
    }
});
