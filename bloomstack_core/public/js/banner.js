$(document).ready(function () {
    if (frappe.boot.staging_server == true) {
        let $banner = $(
            `<div class="bloomstack-banner">
            <span class="notice">Notice : This is a staging instance</span>
        </div>`
        );
        $('body').append($banner);
        // and finally display it:
        $('body').addClass('has-banner');
    }
});