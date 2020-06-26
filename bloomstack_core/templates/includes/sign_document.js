$(document).ready(function () {
	var body = $('.third-party-sign')
	var $sigdiv = $("#signature");
	$sigdiv.jSignature({
		height: 300,
		width: (body.width() - 5),
		lineWidth: 3
	});   // inits the jSignature widget.
	$sigdiv.jSignature("reset");   // clears the canvas and rerenders the decor on it.

	$("#signeeDetails input[type='radio']").click(function(){
		if ( $(this).attr('value') == 'PartyTypeCompany' ) {
			$('.partytypecompany').show();
		} else {
			$('.partytypecompany').hide();
		}
	});

	$(".refresh-signature").on("click", function () {
		$sigdiv.jSignature("reset"); 
	});

	$("#approveDocument").on("click", function () {
		var sign = $sigdiv.jSignature("getData");
		var signee = $("#signee").val();
		var party_business_type = $("#signeeDetails input[name='type']:checked").val();
		var designation;
		if(party_business_type === "PartyTypeIndividual") {
			designation = "NA";
		}
		else {
			designation = $("#signee-designation").val();
		}

		// proceed only if user has put signature and signee name.
		if (signee && $sigdiv.jSignature("getData", "native").length > 0 && designation) {
			$(".user-signature").hide();
			frappe.call({
				method: "bloomstack_core.utils.authorize_document",
				args: {
					sign: sign,
					signee: signee,
					docname: "{{ auth_req_docname }}",
					party_business_type: party_business_type,
					designation: designation
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
							$(".contract").html('The contract is authorized. Please check your email for the signed copy of the document.');
						}
					})
				}
			});
		}
		else {
			frappe.throw(__("Please enter your name, signature and designation"));
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
