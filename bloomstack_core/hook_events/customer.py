import frappe
from frappe import _

def validate_customer_window(customer, method):
    if(customer.delivery_start_time > customer.delivery_stop_time):
        return frappe.throw(_("Customer start window should be before customer end window"))
