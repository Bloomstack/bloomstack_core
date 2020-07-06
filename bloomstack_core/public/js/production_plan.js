frappe.ui.form.on("Production Plan Item", "bom_no", function(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	if (row.bom_no) {
		let workstations_value = []
		frappe.model.with_doc("BOM", row.bom_no, function() {
			let bom_doc = frappe.model.get_doc("BOM", row.bom_no);
			$.each(bom_doc.operations, function(i, s) {
				workstations_value.push(s.workstation)
			});
			row.workstations = workstations_value.join(", ")
			frm.refresh_field("po_items");
		});
	}
});