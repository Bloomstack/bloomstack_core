/* global frappe, bloomstack */

bloomstack.track_and_trace.modules.add("Stock Entry", {
    fields: [
        { field: "work_order", label: "Work Order"},
        { field: "posting_date", label: "Posting Date", fieldtype: "Date"}
    ],

    icon: "fa fa-archive"

});

bloomstack.track_and_trace.modules.add("Stock Entry Detail", {
    fields: [
        { field: "s_warehouse", label: "Source Warehouse" },
        { field: "t_warehouse", label: "Target Warehouse" },
        { field: "item_name", label: "Item Name" },
        { field: "qty", label: "Qty" },
        { field: "stock_uom", label: "UOM" },
        { field: "batch_no", label: "Batch No" },
        { field: "serial_no", label: "Serial No" }
    ],
    
    icon: "fa fa-archive",

    has_route: false,

    format(data) {
        
        let entry = data.data;
        data.title = `${entry.item_code}: ${entry.item_name}`;

        if ( data.data.serial_no ) {
            let serials = data.data.serial_no.split(/\\n+|,/);
            if ( serials.length === 1 ) {
                if ( serials[0] === data.search_dn ) {
                    data.data.serial_no = data.search_dn;
                }
            } else {
                data.data.serial_no = "MULTIPLE";
            }

            if ( serials.length > 0 ) {
                for(let serial of serials) {
                    data.children.push({
                        query: true,
                        search_dt: data.search_dt,
                        search_dn: data.search_dn,
                        dt: "Serial No",
                        dn: serial
                    })
                }
            }
        }

        if ( data.data.batch_no ) {
            // preemptively adds a child node to be queried when this node is
            // expanded by the user.
            data.children.push({
                query: true,
                search_dt: data.search_dt,
                search_dn: data.search_dn,
                dt: "Batch",
                dn: data.data.batch_no
            })
        }

        // remove source warehouse from fields if not present
        if ( entry.s_warehouse ) {
            // we'll pepper in additional icon for input for UX
            data.title = `<li class="fa fa-arrow-right" title="Input"></li> ${data.title}`;
        }

        // remove target warehouse from fields if not present
        if ( entry.t_warehouse ) {
            // we'll pepper in additional icon for outpuy for UX
            data.title = `<li class="fa fa-arrow-left" title="output"></li> ${data.title}`;
        }

        return bloomstack.get_value("Item", "image", { name: entry.item_code })
            .then((result) => {
                data.image_path = result.image;
                return data;
            })
    }
});
