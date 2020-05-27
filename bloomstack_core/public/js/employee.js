frappe.form.link_formatters['Employee'] = function(value, doc) {
  if (!doc) {
    return value
  }
  if (doc.employee_name) {
    return doc.employee_name;
  } 
  else {
    frappe.db.get_value("Employee", { "name" : value }, "employee_name", (r) => {
      employee_name = r.employee_name;
    });
    return employee_name;
  }
}
