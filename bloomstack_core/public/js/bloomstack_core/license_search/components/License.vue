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
                <p><a href="#" @click.prevent="make_compliance_info(make_customer)" class="conversion-actions">Convert to lead</a></p>
                <p><a href="#" @click.prevent="make_compliance_info(make_customer)" class="conversion-actions">Convert to customer</a></p>
                <p><a href="#" @click.prevent="make_compliance_info(make_supplier)" class="conversion-actions">Convert to supplier</a></p>
        </div>
    </div>
</template>

<script>

    import FrappeService from "../services/frappe_service";

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
            quick_entry(doctype, fieldMap) {
                const mapper = {};
                for(let customerField in fieldMap) {
                    let licenseField = fieldMap[customerField];
                    mapper[customerField] = this.license[licenseField];
                }

                frappe.new_doc("Customer", false, function(dialog) {
                    dialog.set_values(mapper);
                });
            },

            make_compliance_info: function(callee) {
                const complianceInfo = {
                    "doctype": "Compliance Info",
                    "license_number": this.license.license_number
                }
                return FrappeService.insertDoc({
                    doc: complianceInfo,
                    isFieldExist: "license_number"
                 }).then(res => {
                     callee();
                }).catch(err => {
                    callee();
                });
            },

            make_customer() {
                const fieldMap = {
                    customer_name: "legal_name",
                    email_id: "email_id",
                    mobile_no: "phone",
                    license: "license_number"
			    };

                this.quick_entry("Customer", fieldMap);
            },

            make_lead() {
                const fieldMap = {
                    customer_name: "legal_name",
                    email_id: "email_id",
                    mobile_no: "phone",
                    license: "license_number"
			    };

                this.quick_entry("Lead", fieldMap);
            },

            make_supplier() {
                const fieldMap = {
                    customer_name: "legal_name",
                    email_id: "email_id",
                    mobile_no: "phone",
                    license: "license_number"
			    };

                this.quick_entry("Supplier", fieldMap);
            }
        }
    }
</script>

<style>

</style>