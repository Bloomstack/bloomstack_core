frappe.ui.form.on("Purchase Order Item", {
	amount: function(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		console.log("AMOUNT", row.amount)
		if(row.qty != 0){
			let rate = row.amount/row.qty;
			frappe.model.set_value(cdt, cdn, "rate", rate);
			console.log("RATE", rate) 
		}
	}
})