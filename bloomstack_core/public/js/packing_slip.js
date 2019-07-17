frappe.ui.form.on('Packing Slip', {
    delivery_note: function(frm) {
        frappe.db.get_value('Delivery Note', {name: frm.doc.delivery_note}, 'company', (r) => {
            frm.set_value("company", r.company)
        });

        erpnext.queries.setup_queries(frm, "Warehouse", function() {
            return erpnext.queries.warehouse(frm.doc);
		});
    },
    source_warehouse: function(frm) {
		if(frm.doc.source_warehouse) {
			$.each(frm.doc.items || [], function(i, item) {
				frappe.model.set_value(frm.doctype + " Item", item.name, "source_warehouse", frm.doc.source_warehouse);
			});
		}
    },
    target_warehouse: function(frm) {
        if(frm.doc.target_warehouse) {
			$.each(frm.doc.items || [], function(i, item) {
				frappe.model.set_value(frm.doctype + " Item", item.name, "target_warehouse", frm.doc.target_warehouse);
			});
        }    
    }
});
