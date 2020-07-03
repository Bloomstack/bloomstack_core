frappe.ui.form.on("Production Plan Item", "bom_no", function(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	if (row.bom_no) {
		frappe.model.with_doc("BOM", row.bom_no, function() {
			let bom_doc = frappe.model.get_doc("BOM", row.bom_no);
			let workstations_value = '';
			$.each(bom_doc.operations, function(i, s) {
				workstations_value += s.workstation + ", "
			});
			row.workstations = workstations_value;
			frm.refresh_field("po_items");
		});
	}
});