frappe.ready(function () {
	frappe.web_form.events.on('after_load', () => {
		frappe.web_form.on('status', (field, value) => {
			if (value === 'Closed') {
				$('.web-form-actions .btn-danger').remove();
				frappe.web_form.add_button("Reopen", "danger", () => {
					var d = new frappe.ui.Dialog({
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
							frappe.web_form.set_value('status', "Open");
						}
					});
					d.show();
				});
			} else {
				$('.web-form-actions .btn-danger').remove();
				frappe.web_form.add_button("Close", "danger", () => {
					frappe.web_form.set_value('status', "Closed");
				});
			}
		});
	});
})