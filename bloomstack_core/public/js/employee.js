let employee_name;
frappe.form.link_formatters['Employee'] = function(value, doc) {
  if (!value) {
    frappe.msgprint({
      title: __('Error'),
      indicator: 'red',
      message: __('Please enter a valid Employee Code')
  });
  }
  else {
    if (!doc) {
      return value
    }
    if (doc.employee_name) {
      return doc.employee_name;
    } 
    else {
      frappe.db.get_value("Employee", { "name" : value }, "employee_name", (r) => {
        if(r.employee_name == '') {
          employee_name = value
        }
        else {
          employee_name = r.employee_name;
        }
      });
      return employee_name;
    }
  }
}
