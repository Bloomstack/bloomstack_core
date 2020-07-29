import frappe
from bloomstack_core.hook_events.delivery_trip import get_address_display
from frappe.utils import add_days, getdate, nowdate

API_VERSION = "v1.0"


@frappe.whitelist()
def trips(driver_email):
	"""
	Get all trips assigned to the given driver.

	Args:
		driver_email (str): The email address of the driver

	Returns:
		dict: The Delivery Trips assigned to the driver, along with customer and item data
	"""

	trips_data = []
	driver_trips = frappe.get_all("Delivery Trip", filters=get_filters(driver_email), fields=["name"])

	for trip in driver_trips:
		trip_doc = frappe.get_doc("Delivery Trip", trip.name)
		trip_data = build_trip_data(trip_doc)
		trips_data.append(trip_data)

	return {
		"version": API_VERSION,
		"trips": trips_data
	}


def get_filters(email):
	return {
		"docstatus": 1,
		"driver": frappe.db.get_value("Driver", {"user_id": email}, "name"),
		"departure_time": ["BETWEEN", [add_days(getdate(nowdate()), -60), getdate(nowdate())]]
	}


def build_item_data(stop):
	items_data = []
	dn_doc = frappe.get_doc("Delivery Note", stop.delivery_note)
	for item in dn_doc.items:
		items_data.append({
			"name": item.item_code,
			"qty": item.qty,
			"unitPrice": item.rate
		})
	return items_data


def build_stop_data(trip):
	stops_data = []
	for stop in trip.delivery_stops:
		stops_data.append({
			"name": stop.name,
			"address": get_address_display(stop.address),
			"customer": stop.customer,
			"amountToCollect": stop.grand_total,
			"deliveryNote": stop.delivery_note,
			"salesInvoice": stop.sales_invoice,
			"items": build_item_data(stop),
			"distance": stop.distance,
			"earliestDeliveryTime": stop.delivery_start_time,
			"latestDeliveryTime": stop.delivery_end_time,
			"estimatedArrival": stop.estimated_arrival,
			"customerPhoneNumber": frappe.db.get_value("Address", stop.address, "phone")
		})
	return stops_data


def build_trip_data(trip):
	return {
		"name": trip.name,
		"status": trip.status,
		"vehicle": trip.vehicle,
		"company": trip.company,
		"stops": build_stop_data(trip)
	}
