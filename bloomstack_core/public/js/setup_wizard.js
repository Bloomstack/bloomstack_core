frappe.provide("bloomstack.setup");


frappe.setup.on("before_load", function () {
    frappe.setup.remove_slide("domain");
    bloomstack.setup.slides_settings.map(frappe.setup.add_slide);
});

bloomstack.setup.slides_settings = [
    {
    // Domain
    name: 'domain',
    title: __('Pick your domains'),
    fields: [
        {
            fieldname: 'domains',
            label: __('Domains'),
            fieldtype: 'MultiCheck',
            options: [
                { "label": __("Distributor"), "value": "Distribution" },
                { "label": __("Manufacturer"), "value": "Manufacturing" },
                { "label": __("Retailer"), "value": "Retail" },
                { "label": __("Cultivator (beta)"), "value": "Agriculture" },
            ], reqd: 1
        },
    ],
    // help: __('Select the nature of your business.'),
    validate: function () {
        if (this.values.domains.length === 0) {
            frappe.msgprint(__("Please select at least one domain."));
            return false;
        }

        this.values.domains.push("Services")
        frappe.setup.domains = this.values.domains;
        return true;
    },
},
    ];