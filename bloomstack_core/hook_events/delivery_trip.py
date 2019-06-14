from frappe.model.document import Document
import frappe


def set_vehicle_last_odometer_value(self, event):
    print("reached here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if self.actual_distance_travelled:
        vehicle = frappe.get_doc("Vehicle", self.vehicle)
        vehicle.update({"last_odometer": self.odometer_stop_value})
        vehicle.save()
