$(document).ready(function() {
    if (frappe.boot.staging_server == true) {
        $('body').append($('<div class="bloomstack-banner"><button type="button" class="btn close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button> </div>'));
        // get banner ref
        let $banner = $('.bloomstack-banner');

        // empty banner in case there was something in it before hand:
        $banner.empty();

        // add your content
        $banner.text("Notice : This is a staging instance");

        // and finally display it:
        $('body').addClass('has-banner')
    }
});