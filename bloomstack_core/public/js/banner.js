$(document).ready(function() {
    if (frappe.boot.staging_server == true) {
    let $banner = $(
        `<div class="bloomstack-banner">
            <span class="notice">Notice : This is a staging instance</span>
            <button type="button" class="btn close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">×</span>
            </button>
        </div>`
     );    
    $('body').append($banner);
    $banner.find("button").click(function(){
        $banner.remove();
    });
        // and finally display it:
        $('body').addClass('has-banner');
}
});