<template>
    <div class="license-card row">
        <div class="col-md-3 col-sm-3 col-xs-3">
            <div class="map">
              <a href="">
                <img src="assets/bloomstack_core/images/map.png" alt="">
                <span>view map</span>
              </a>
            </div>
            <div class="actions">
                <p><a href="" class="conversion_actions">Convert to lead</a></p>
                <p><a href="" class="conversion_actions">Convert to customer</a></p>
                <p><a href="" class="conversion_actions">Convert to supplier</a></p>
            </div>
        </div>
        <div class="col-md-9 col-sm-9 col-xs-9">
            <div class="row license_info">
                <div class="col-md-4 col-sm-6 col-xs-6 legal_name">{{ license.legal_name }}</div>
                <div class="col-md-4 col-sm-6 col-xs-6 license_number">{{ license.license_number }}</div>
                <div class="col-md-4 col-sm-12 col-xs-12 license_type">{{ license.license_type }}</div>
            </div>
            <div class="row license_info">
                <p>{{ license.zip_code }}|{{ license.county }}|{{ license.city }}</p>
                <p>{{ license.email_id }}</p>
                <p>License expiry: {{ license.expiration_date }}</p>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            license: Object
        }
    }
    $('license-card').click(function() {
        $('license-card .actions').toggleClass("show");
    });
</script>

<style>

</style>