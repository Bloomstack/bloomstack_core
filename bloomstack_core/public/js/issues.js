frappe.ready(function () {
	frappe.web_form.events.on('after_load', () => {
		// To check whether new or edited
		if (!frappe.web_form.is_new) {
			frappe.web_form.set_df_property('subject', 'read_only', 1);
			frappe.web_form.set_df_property('description', 'read_only', 1);
			frappe.web_form.set_df_property('attachment', 'read_only', 1);
			if (!frappe.web_form.doc.attachment) {
				frappe.web_form.set_df_property('attachment', 'hidden', 1);
			}

			$('.web-form-actions .btn-primary, .web-form-footer .btn-primary').hide();
		}

		frappe.web_form.on('status', (field, value) => {
			if (value === 'Closed') {
				$('.web-form-actions .btn-danger').remove();
				frappe.web_form.add_button("Reopen", "secondary", () => {
					var d = new frappe.ui.Dialog({
						'title': 'Enter reason',
						'fields': [{
							'fieldname': 'comment',
							'fieldtype': 'Text',
							'label': "Reason to reopen",
							'reqd': 1
						}],
						primary_action: function () {
							d.hide();
							$('#comment-form').show();
							$('.add-comment.btn').hide();
							data = d.get_values();
							$("#comment-form [name='comment_by']").val(frappe.full_name);
							$("#comment-form [name='comment_email']").val(frappe.user_id);
							$("#comment-form [name='comment']").append(data.comment);
							$('#submit-comment').click();
							frappe.web_form.doc.status = 'Open';
							frappe.web_form.save();
						}
					});
					d.show();
				});
			} else {
				$('.web-form-actions .btn-danger').remove();
				frappe.web_form.add_button("Close", "danger", () => {
					frappe.confirm(__("Are you sure you want to close this Issue?"), function () {
						frappe.web_form.doc.status = 'Closed';
						frappe.web_form.save();
					})
				});
			}
		});
	});
})
