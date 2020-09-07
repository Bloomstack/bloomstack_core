export default {
    insertDoc({doc, isFieldExist}) {
        return new Promise(function (resolve, reject) {
            frappe.db.exists(doc.doctype, doc[isFieldExist]).then(function(response) {
                if(response) {
                    reject(response);
                    return;
                }

                frappe.db.insert(doc).then(function(response) {
                    resolve(response);
                })
            })
		});
    }
}