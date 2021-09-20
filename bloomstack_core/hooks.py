# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "bloomstack_core"
app_title = "Bloomstack Core"
app_publisher = "Bloom Stack, Inc"
app_description = "Core Bloomstack App"
app_icon = "octicon octicon-gear"
app_color = "light green"
app_email = "developers@bloomstack.com"
app_license = "MIT"
app_logo_url = '/assets/bloomstack_core/images/icon.png'


# Set setup defaults
setup_wizard_requires = "/assets/bloomstack_core/js/setup_wizard.js"
setup_wizard_stages = "bloomstack_core.setup.setup_wizard.get_setup_stages"

# Set website defaults
login_mail_title = "New Bloomstack Account"
error_report_email = "support@bloomstack.com"
website_context = {
	"favicon": "/assets/bloomstack_core/images/favicon.ico",
	"splash_image": "/assets/bloomstack_core/images/splash.png"
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_js = [
	"/assets/bloomstack_core/js/query_report.js",
	"/assets/bloomstack_core/js/banner.js",
	"/assets/js/bloomstack_desk.js"
]
app_include_css = [
	"/assets/bloomstack_core/css/buttons.css",
	"/assets/bloomstack_core/css/trees.css",
	"/assets/bloomstack_core/css/mobile-fixes.css",
	"/assets/bloomstack_core/css/banner.css",
	"/assets/bloomstack_core/css/desk.css",
	"/assets/bloomstack_core/css/order_desk.css",
	"/assets/bloomstack_core/css/contract.css",
	"/assets/css/reports.min.css"
]

# include js, css files in header of web template
web_include_css = [
	"/assets/bloomstack_core/css/buttons.css",
	"/assets/bloomstack_core/css/login.css"
]
# web_include_js = "/assets/bloomstack_core/js/bloomstack_core.js"

# include js, css files in header of web form
webform_include_js = {
	"Issue": "public/js/issues.js"
}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Batch": "public/js/batch.js",
	"Compliance Settings": "public/js/compliance_settings.js",
	"Delivery Note": "public/js/delivery_note.js",
	"Delivery Trip": "public/js/delivery_trip.js",
	"Driver": "public/js/driver.js",
	"Item": "public/js/item.js",
	"Packing Slip": "public/js/packing_slip.js",
	"Pick List": "public/js/pick_list.js",
	"Quality Inspection": "public/js/quality_inspection.js",
	"Sales Order": "public/js/sales_order.js",
	"Work Order": "public/js/work_order.js",
}

doctype_list_js = {
	"Sales Order": "public/js/sales_order_list.js",
	"Purchase Order": "public/js/purchase_order_list.js",
	"Purchase Invoice": "public/js/purchase_invoice_list.js"
}

# override_doctype_dashboards = {
# }

# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
doctype_calendar_js = {
	"Work Order": "public/js/work_order_calendar.js"
}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "bloomstack_core.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "bloomstack_core.install.before_install"
# after_install = "bloomstack_core.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

notification_config = "bloomstack_core.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	("Company", "Supplier", "Customer"): {
		"validate": [
			"bloomstack_core.hook_events.utils.validate_default_license",
			"bloomstack_core.hook_events.utils.validate_expired_licenses"
		]
	},
	"Delivery Note": {
		"validate": "bloomstack_core.hook_events.delivery_note.link_invoice_against_delivery_note",
		"before_submit": [
			"bloomstack_core.hook_events.delivery_note.link_invoice_against_delivery_note"
		],
		"on_submit": "bloomstack_core.hook_events.delivery_note.create_integration_request",
		"on_update_after_submit": "bloomstack_core.hook_events.delivery_note.link_invoice_against_delivery_note"
	},
	"Delivery Trip": {
		"validate": [
			"bloomstack_core.hook_events.delivery_trip.generate_directions_url",
			"bloomstack_core.hook_events.delivery_trip.link_invoice_against_trip"
		],
		"on_submit" : "bloomstack_core.hook_events.delivery_trip.make_transfer_templates",
		"on_update_after_submit": "bloomstack_core.hook_events.delivery_trip.set_vehicle_last_odometer_value",
	},
	"Item": {
		"on_update": "bloomstack_core.hook_events.item.create_integration_request"
	},
	"Sales Invoice": {
		"before_submit": "bloomstack_core.hook_events.sales_invoice.create_metrc_sales_receipt",
		"before_update_after_submit": "bloomstack_core.hook_events.sales_invoice.set_invoice_status"
	},
	"User": {
		"after_insert": "bloomstack_core.hook_events.user.update_bloomtrace_user"
	},
	("Sales Order", "Delivery Note"): {
		"validate": "bloomstack_core.hook_events.utils.validate_delivery_window",
		"on_submit": "bloomstack_core.hook_events.utils.validate_delivery_window"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"bloomstack_core.hook_events.item.execute_bloomtrace_integration_request",
		"bloomstack_core.hook_events.delivery_note.execute_bloomtrace_integration_request"
	],
	"hourly": [
		"bloomstack_core.hook_events.user.execute_bloomtrace_integration_request"
	]
}

after_migrate = [
	'bloomstack_core.hook_events.cognito.setup'
]

# Testing
# -------

# before_tests = "bloomstack_core.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
