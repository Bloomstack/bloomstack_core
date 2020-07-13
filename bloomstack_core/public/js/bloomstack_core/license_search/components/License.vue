<template>
    <div class="license-card">
        <div class="" @click="makeCustomer()">
            Click me to add a new customer
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
    // import Vuex from './../../../../node_modules/vuex/dist/vuex';

    export default {
        props: {
            license: Object
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