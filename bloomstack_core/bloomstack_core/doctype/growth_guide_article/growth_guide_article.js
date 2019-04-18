// Copyright (c) 2019, Bloom Stack, Inc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Growth Guide Article', {
	refresh: function (frm) {
		frm.set_query("doc_type", "references", (frm, cdt, cdn) => {
			return { filters: { "istable": 0 } }
		})
	}
});
