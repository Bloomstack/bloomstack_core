$(document).ready(function () {
	var $sigdiv = $("#signature");
	$sigdiv.jSignature();   // inits the jSignature widget.
	$sigdiv.jSignature("reset");   // clears the canvas and rerenders the decor on it.

	$("#approveDocument").on("click", function () {
		var sign = $sigdiv.jSignature("getData");
		var signee = $("#signee").val();
		var printBtn = jQuery('.printBtn').clone();
		if ($sigdiv.jSignature('getData', 'native').length != 0 && signee) {   // proceed only if user has put signature and signee name.
			$(".user-signature").hide();

			frappe.call({
				method: "bloomstack_core.utils.authorize_document",
				args: {
					sign: sign,
					signee: signee,
					docname: "{{ auth_req_docname }}",
				},
				freeze: true,
				callback: (r) => {
					frappe.call({
						method: "bloomstack_core.www.authorize_document.custom_print_doc",
						args: {
							auth_req_docname: "{{ auth_req_docname }}"
						},
						callback: (r) => {
							$(".title").html("The {{doc.doctype}} has been signed and has been emailed to you at {{authorizer_email}}");
							$(".contract").html(r.message);
							$(".contract").show();
							printBtn.appendTo('.col-lg-4');
							
						}
					})
				}
			});
		}
		else {

			frappe.throw(__("Please put your name and signature."));
		}
	});

	$("#rejectDocument").on("click", function () {
		$(".user-signature").hide();
		frappe.call({
			method: "bloomstack_core.utils.reject_document",
			args: {
				docname: "{{ auth_req_docname }}",
			},
			freeze: true,
			callback: (r) => {
				frappe.msgprint(__("The document has been rejected by you!"));
			}
		})
	});
});