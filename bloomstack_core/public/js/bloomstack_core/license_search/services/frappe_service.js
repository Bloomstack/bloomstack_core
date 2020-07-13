export default {
    insertDoc(doc) {
        console.log({ doc, isFieldExist });
        return new Promise(function (resolve, reject) {
            frappe.db.exists(doc.doctype, doc[isFieldExist]).then(function(response) {
                console.log(response);
                if(response) {
                    reject(response);
                }

                frappe.db.insert(doc).then(function(response) {
                    console.log("insert", response)
                    resolve(response);
                })
            })
		});
    }
}