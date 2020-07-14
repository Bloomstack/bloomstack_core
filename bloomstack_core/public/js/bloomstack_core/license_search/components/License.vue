<template>
    <div class="license-card row" v-bind:class="{ 'is-open': toggle }" @click="toggle = !toggle">
        <div class="col-md-3 col-sm-3 col-xs-3">
            <div class="map">
              <a href="">
                <img src="assets/bloomstack_core/images/map.png" alt="">
                <span>view map</span>
              </a>
            </div>
        </div>
        <div class="col-md-9 col-sm-9 col-xs-9">
            <div class="row license-info">
                <div class="col-md-4 col-sm-6 col-xs-6 legal-name">{{ license.legal_name }}</div>
                <div class="col-md-4 col-sm-6 col-xs-6 license-number">{{ license.license_number }}</div>
                <div class="col-md-4 col-sm-12 col-xs-12 license-type">{{ license.license_type }}</div>
            </div>
            <div class="row license-info">
                <p>{{ license.zip_code }}|{{ license.county }}|{{ license.city }}</p>
                <p>{{ license.email_id }}</p>
                <p>License expiry: {{ license.expiration_date }}</p>
            </div>
        </div>
        <div class="actions">
                <p><a href="" class="conversion-actions">Convert to lead</a></p>
                <p><a href="" class="conversion-actions">Convert to customer</a></p>
                <p><a href="" class="conversion-actions">Convert to supplier</a></p>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            license: Object
        },
        data() {
            return {
                toggle: false
            }
        },
        methods: {
            makeCustomer() {
                const customer = {
                    "doctype": "Customer",
                    "customer_name": this.license.business_owner || this.license.legal_name,
                    "customer_group": "Individual",
                    "territory": "All Territories",
                    "customer_type": "Company"
                };
                this.$store.dispatch('makeCustomer', customer);
            },

            makeLead() {
                const lead = {
                    "doctype": "Customer",
                    "customer_name": this.license.business_owner || this.license.legal_name,
                    "customer_group": "Individual",
                    "territory": "All Territories",
                    "customer_type": "Company"
                };
                this.$store.dispatch('makeCustomer', lead);
            },

            makeSupplier() {
                const supplier = {
                    "doctype": "Customer",
                    "customer_name": this.license.business_owner || this.license.legal_name,
                    "customer_group": "Individual",
                    "territory": "All Territories",
                    "customer_type": "Company"
                };
                this.$store.dispatch('makeCustomer', supplier);
            }
        }
    }
</script>

<style>

</style>