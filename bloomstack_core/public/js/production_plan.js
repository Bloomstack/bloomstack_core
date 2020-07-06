frappe.ui.form.on("Production Plan Item", {
    bom_no: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.bom_no) {
			frappe.model.with_doc("BOM", row.bom_no, function() {
				let bom_doc = frappe.model.get_doc("BOM", row.bom_no);
				let workstations = bom_doc.operations.map(operation => operation.workstation);
				row.workstations = workstations.join('\n');
				frm.refresh_field("po_items");
			});
		}
    }
});