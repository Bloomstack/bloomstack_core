export default {
    getLicenses({ pageNum, perPage, filters }) {
        return new Promise(function (resolve, reject) {
            frappe.call({
                method: "bloomstack_core.bloomstack_core.page.license_search.license_search.get_all_licenses",
                args: {
                    page_number: pageNum,
                    per_page: perPage,
                    filters: filters
                },
                callback: function(response) {
                    // console.log(response.message)
                    resolve(response.message);
                }
            })
		});


    }
}