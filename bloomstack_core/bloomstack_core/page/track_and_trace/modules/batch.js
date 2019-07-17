/* global frappe, bloomstack */

bloomstack.track_and_trace.modules.add("Batch", {
    fields: [
        { field: "item", label: "Item" },
        { field: "manufacturing_date", label: "Manufacturing Date", fieldtype: "Date" },
        { field: "supplier", label: "Supplier" },
    ],

    icon: "fa fa-th-large",

    format(data) {
        let batch = data.data;


        if ( batch.reference_doctype && batch.reference_name ) {
            data.children.push({
                query: true,
                dt: batch.reference_doctype,
                dn: batch.reference_name,
                search_dt: data.search_dt,
                search_dn: data.search_dn
            });
        }

        return bloomstack.get_value("Item", "item_name", { name: batch.item})
            .then((v) => {
                batch.item = `<a data-route-dt="Item" data-route-dn="${batch.item}">${v.item_name} (${batch.item})</a>`;
            })
            .then(() => {
                return Promise.resolve(frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Stock Ledger Entry",
                        fields: ["name"],
                        filters: [["batch_no", "=", batch.name], ["actual_qty", ">", 0]],
                        order_by: "creation DESC",
                        limit_page_length: 9999
                    }
                }));
            })
            .then((r) => {
                if ( r.message ) {
                    data.children.push({
                        query: false,
                        dt: "report#Stock Ledger/Positive",
                        dn: data.dn,
                        search_dt: data.search_dt,
                        search_dn: data.search_dn,
                        image_path: null,
                        icon: "fa fa-arrow-up positive",
                        title: "Stock Inputs",
                        fields: [],
                        parents: Object.assign({}, data.parents || {}),
                        children: r.message.map((row) => ({
                            query: true,
                            dt: "Stock Ledger Entry",
                            dn: row.name,
                            search_dt: data.search_dt,
                            search_dn: data.search_dn
                        }))
                    })
                }
            })
            .then(() => {
                return Promise.resolve(frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Stock Ledger Entry",
                        fields: ["name"],
                        filters: [["batch_no", "=", batch.name], ["actual_qty", "<", 0]],
                        order_by: "creation DESC",
                        limit_page_length: 9999
                    }
                }));
            })
            .then((r) => {
                if ( r.message ) {
                    data.children.push({
                        query: false,
                        dt: "report#Stock Ledger/Negative",
                        dn: data.dn,
                        search_dt: data.search_dt,
                        search_dn: data.search_dn,
                        image_path: null,
                        icon: "fa fa-arrow-down negative",
                        title: "Stock Outputs",
                        fields: [],
                        parents: Object.assign({}, data.parents || {}),
                        children: r.message.map((row) => ({
                            query: true,
                            dt: "Stock Ledger Entry",
                            dn: row.name,
                            search_dt: data.search_dt,
                            search_dn: data.search_dn
                        }))
                    })
                }
            })
            .then(() => {
                return data;
            });
    }

});