import frappe


def configure_selling_settings():
	# Remove default territory and customer group
	selling_settings = frappe.get_single("Selling Settings")
	selling_settings.territory = None
	selling_settings.customer_group = None
	selling_settings.save()


def configure_stock_settings():
	# Avoid auto-selecting batches for state compliance
	stock_settings = frappe.get_single("Stock Settings")
	stock_settings.automatically_set_batch_nos_based_on_fifo = False
	stock_settings.save()


def configure_system_settings():
	system_settings = frappe.get_single("System Settings")
	system_settings.float_precision = 2
	system_settings.currency_precision = 2
	system_settings.save()


def disable_standard_reports():
	frappe.db.set_value("Report", "Addresses And Contacts", "disabled", 1)
