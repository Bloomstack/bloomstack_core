$(document).ready(function () {
    var $sigdiv = $("#signature");
    $sigdiv.jSignature();   // inits the jSignature widget.
    $sigdiv.jSignature("reset");   // clears the canvas and rerenders the decor on it.

    $("#approveDocument").on("click", function () {
        var sign = $sigdiv.jSignature("getData");
        var signee = $("#signee").val();
        if ($sigdiv.jSignature('getData', 'native').length != 0 && signee) {   // proceed only if user has put signature and signee name.
            $(".user-signature").hide();
            $(".contract").hide();

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
							$(".title").html("You have signed the below {{doc.doctype}}!");
							$(".contract").html(r.message);
                            $(".contract").show();
                            $(".signed-doc-actions").show();
						}
					})
                }
            });
        }
        else {

            frappe.throw(__("Please put your name and signature!"));
        }
    });

    $("#printBtn").on("click", function () {
        console.log("print format", '{{print_format}}');
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