$(document).ready(function () {
    var $sigdiv = $("#signature")
    $sigdiv.jSignature();
    $sigdiv.jSignature("reset");

$("#step2").on("click", function () {
    var sign = $sigdiv.jSignature("getData");
    var signee = document.getElementById("signee").value;
    if (!($sigdiv.jSignature('getData', 'native').length == 0) && signee) {
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
                frappe.msgprint(__("The document has been approved by you!"));
            }
        })
    }
    else{
        alert('Please enter Sign and Signee ');
     }
});
});