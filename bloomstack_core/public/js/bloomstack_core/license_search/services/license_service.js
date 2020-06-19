export default {
    baseUrl: "https://bloomtrace.io",
    getLicenses({ pageNum, perPage, filters }) {
        const fields = [
            "legal_name",
            "status",
            "license_number",
            "license_type",
            "expiration_date",
            "email_id",
            "county",
            "city",
            "zip_code",
            "business_structure"
        ];

        return new Promise(function (resolve, reject) {
            frappe.call({
                method: "bloomstack_core.bloomstack_core.page.license_search.license_search.get_all_licenses",
                args: {
                    page_number: pageNum,
                    per_page: perPage,
                    filters: filters
                },
                callback: function(response) {
                    console.log(response);
                    resolve(response.message);
                }
            })
		});


    }
}