$(document).ready(function () {
	let body = $('.third-party-sign');
	let $sigdiv = $("#signature");

	// init the jSignature widget
	$sigdiv.jSignature({
		height: 300,
		width: (body.width() - 5),
		lineWidth: 3
	});

	// clear the canvas and re-render the decor on it
	$sigdiv.jSignature("reset");

	$("#signeeDetails input[type='radio']").click(function () {
		if ($(this).data("party-type") === "Company") {
			$(".party-type-company").show();
		} else {
			$(".party-type-company").hide();
		}
	});

	$(".refresh-signature").on("click", function () {
		$sigdiv.jSignature("reset");
	});

	$("#approveDocument").on("click", function () {
		let sign = $sigdiv.jSignature("getData");
		let signee = $("#signee").val();
		let party_business_type = $("#signeeDetails input[name='type']:checked").val();
		let designation;

		if (party_business_type === "Individual") {
			designation = "NA";
		} else {
			designation = $("#signee-designation").val();
		}

		// proceed only if user has put name, signature and designation
		if (!(signee && $sigdiv.jSignature("getData", "native").length > 0 && designation)) {
			frappe.throw(__("Please enter your name, signature and designation"));
		}

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
				});
			}
		});
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
