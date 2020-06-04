$(document).ready(function () {
	var $sigdiv = $("#signature");
	$sigdiv.jSignature();   // inits the jSignature widget.
	$sigdiv.jSignature("reset");   // clears the canvas and rerenders the decor on it.

	$(".refresh_signature").on("click", function () {
		$sigdiv.jSignature("reset"); 
	});

	$("#approveDocument").on("click", function () {
		var sign = $sigdiv.jSignature("getData");
		var signee = $("#signee").val();

		// proceed only if user has put signature and signee name.
		if (signee && $sigdiv.jSignature('getData', 'native').length != 0) {
			$(".user-signature").hide();
			frappe.call({
				method: "bloomstack_core.utils.authorize_document",
				args: {
					sign: sign,
					signee: signee,
					docname: "{{ auth_req_docname }}"
				},
				freeze: true,
				callback: (r) => {
					frappe.call({
						method: "bloomstack_core.www.authorize_document.custom_print_doc",
						args: {
							auth_req_docname: "{{ auth_req_docname }}"
						},
						callback: (r) => {
							frappe.msgprint(__("The {{ doc.doctype }} has been signed and emailed to you at {{ authorizer_email }}"));
							$(".title").empty();
							$(".contract").html('The contract is authorized. Please check the email for the PDF');
						}
					})
				}
			});
		}
		else {
			frappe.throw(__("Please enter your name and signature"));
		}
	});

	$("#rejectDocument").on("click", function () {
		$(".user-signature").hide();
		frappe.call({
			method: "bloomstack_core.utils.reject_document",
			args: {
				docname: "{{ auth_req_docname }}"
			},
			freeze: true,
			callback: (r) => {
				frappe.msgprint(__("The {{ doc.doctype }} has been rejected"));
			}
		})
	});
});