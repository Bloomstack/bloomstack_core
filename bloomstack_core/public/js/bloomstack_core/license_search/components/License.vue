<template>
    <div class="license-card row" v-bind:class="{ 'is-open': toggle }" @click="toggle = !toggle">
        <div class="col-md-3 col-sm-3 col-xs-3">
            <div class="map">
                <img src="./assets/bloomstack_core/images/map.png" alt="">
                <span>Click here to convert</span>
            </div>
        </div>
        <div class="col-md-9 col-sm-9 col-xs-9">
            <div class="row license-info">
                <div class="col-md-4 col-sm-6 col-xs-6 legal-name">{{ license.legal_name }}</div>
                <div class="col-md-4 col-sm-6 col-xs-6 license-number">{{ license.license_number }}</div>
                <div class="col-md-4 col-sm-12 col-xs-12 license-type">{{ license.license_type }}</div>
            </div>
            <div class="row license-info">
                <p v-if="address">{{ address }}</p>
                <p v-if="license.email_id">{{ license.email_id }}</p>
                <p>License expiry: {{ license.expiration_date }}</p>
            </div>
        </div>
        <div class="actions">
                <a href="#" v-if="!conversion['Lead']" @click.prevent="make_compliance_info(make_lead)" class="conversion-actions">Convert to lead</a>
                <a href="#" v-if="!conversion['Customer']" @click.prevent="make_compliance_info(make_customer)" class="conversion-actions">Convert to customer</a>
                <a href="#" v-if="!conversion['Supplier']" @click.prevent="make_compliance_info(make_supplier)" class="conversion-actions">Convert to supplier</a>
        </div>
    </div>
</template>

<script>

    import FrappeService from "../services/frappe_service";

    export default {
        props: {
            license: Object
        },
        mounted() {
            this.check_entry("Customer");
            this.check_entry("Lead");
            this.check_entry("Supplier");
        },
        data() {
            return {
                toggle: false,
                conversion: {
                    "Customer": false,
                    "Lead": false,
                    "Supplier": false
                }
            }
        },
        computed: {
            address() {
                const addressKeys = ["zip_code", "city", "country"];
                let address = [];
                addressKeys.forEach((key) => {
                    if(this.license[key] != "") {
                        address.push(this.license[key]);
                    }
              	});

              	return (address.join(' | '));
            }
        },
        methods: {
            quick_entry(doctype, fieldMap) {
                const mapper = {};
                for(let field in fieldMap) {
                    let licenseField = fieldMap[field];
                    mapper[field] = this.license[licenseField];
                }

                frappe.new_doc(doctype, mapper, function(dialog) {
                    dialog.set_values(mapper);
                });
            },

            check_entry(doctype) {
                frappe.db.exists(doctype, this.license.legal_name).then((response) => {
                    this.conversion[doctype] = response;
                })
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
                    lead_name: "legal_name",
                    email_id: "email_id",
                    company_name: "legal_name",
                    type_of_business: "business_structure"
			    };

                this.quick_entry("Lead", fieldMap);
            },

            make_supplier() {
                const fieldMap = {
                    supplier_name: "legal_name",
                    license: "license_number"
			    };

                this.quick_entry("Supplier", fieldMap);
            }
        }
    }
</script>

<style>

</style>