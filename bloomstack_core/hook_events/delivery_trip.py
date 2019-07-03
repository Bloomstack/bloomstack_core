import frappe


def set_vehicle_last_odometer_value(trip, method):
	if trip.actual_distance_travelled:
		frappe.db.set_value('Vehicle', trip.vehicle, 'last_odometer', trip.odometer_stop_value)
