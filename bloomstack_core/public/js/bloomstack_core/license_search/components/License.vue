<template>
    <div class="license-card">
        <div class="">

        </div>
        <div class="">
            <div class="">
                <h4>{{ license.legal_name }}</h4>
                <p>{{ license.license_number }}</p>
                <p>{{ license.license_type }}</p>
            </div>
            <div class="">
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
</script>

<style>

</style>