
frappe.ui.form.on('Lead', {
    onload: function(frm) {
        if(frm.doc.status == 'Converted') {
            frappe.db.get_value("Customer", {"lead_name": frm.doc.name}, "creation", (r) => {
				if(r) {
					frm.set_value("account_opened_date", r.creation);
				}	
			});

      }

    }

});