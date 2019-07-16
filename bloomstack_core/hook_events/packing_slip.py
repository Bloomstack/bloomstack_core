import frappe
from frappe.model.mapper import get_mapped_doc


def create_stock_entry(packing_slip_doc, method, target_doc = None):
    print("---------------locals()---------------", locals())
    def set_missing_values(source, target):
        print("---------------locals()---------------", locals())

        target.purpose = "Material Transfer"
        # for i in target.items:
        #     i.t_warehouse = frappe.db.get_single_value("Delivery Settings", "packing_warehouse")

    doc = get_mapped_doc("Packing Slip", packing_slip_doc, {
        "Packing Slip": {
            "doctype": "Stock Entry",
            "validation": {
                "docstatus": ["=", 1]
            }
        },
        "Packing Slip Item": {
            "doctype": "Stock Entry Detail",
            # "field_map": {
                # "stock_qty": "transfer_qty",
                # "batch_no": "batch_no"
            # },
        }
    }, target_doc, set_missing_values)
    doc.save()

# frappe.db.get_single_value