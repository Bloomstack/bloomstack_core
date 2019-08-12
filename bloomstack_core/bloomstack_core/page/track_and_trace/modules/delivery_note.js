/* global frappe, bloomstack */

bloomstack.track_and_trace.modules.add("Delivery Note", {
  fields: [
      { field: "posting_date", label: "Posting Date", fieldtype: "Date" },
      { field: "customer", label: "Customer" },
      { field: "set_warehouse", label: "Source Warehouse" },
      { field: "to_warehouse", label: "To Warehouse" },
      { field: "grand_total", label: "Grand Total", fieldtype: "Currency" },
      { field: "status", label: "Status" }
  ],

  icon: "fa fa-truck"

});

bloomstack.track_and_trace.modules.add("Delivery Note Item", {
  fields: [
    { field: "barcode", label: "Barcode"},
    { field: "item_code", label: "Item Code"},
    { field: "qty", label: "Qty"},
    { field: "uom", label: "UOM"},
    { field: "batch_no", label: "Batch No"},
    { field: "serial_no", label: "Serial No"}
  ],

  icon: "fa fa-list",

  has_route: false,

  format(data) {
    let dni = data.data;

    data.title = `Delivery Node Item: ${dni.item_code}`;

    if ( dni.batch_no ) {
      data.children.push({
        dt: "Batch",
        dn: dni.batch_no,
				search_dt: data.search_dt,
				search_dn: data.search_dn
      })
    }

    if ( dni.serial_no ) {
      data.children.push({
        dt: "Serial No",
        dn: dni.serial_no.split(/\s+/g)[0],
				search_dt: data.search_dt,
				search_dn: data.search_dn
      })
    }

    return data;
  }

});