frappe.ui.form.on("Production Plan Item", "bom_no", function(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	frappe.model.with_doc("BOM", row.bom_no, function() {
		let bom_doc = frappe.model.get_doc("BOM", row.bom_no);
		$.each(bom_doc.operations, function(i, s) {
			row.workstations += s.workstation
		})
	});
});