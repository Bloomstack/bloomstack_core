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
boot_session = "bloomstack_core.boot.boot_session"
login_mail_title = "New Bloomstack Account"
welcome_email = "bloomstack_core.utils.welcome_email"
error_report_email = "support@bloomstack.com"
website_context = {
	"favicon": "/assets/bloomstack_core/images/favicon.ico",
	"splash_image": "/assets/bloomstack_core/images/splash.png"
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_js = [
	"/assets/bloomstack_core/js/conf.js",
	"/assets/bloomstack_core/js/query_report.js",
	"/assets/bloomstack_core/js/banner.js",
	"/assets/js/address_and_contact.min.js",
	"/assets/js/bloomstack_desk.js"
]
app_include_css = [
	"/assets/bloomstack_core/css/buttons.css",
	"/assets/bloomstack_core/css/trees.css",
	"/assets/bloomstack_core/css/mobile-fixes.css",
	"/assets/bloomstack_core/css/banner.css",
	"/assets/bloomstack_core/css/desk.css",
	"/assets/bloomstack_core/css/order_desk.css",
	"/assets/bloomstack_core/css/address_and_contact.css",
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
	"Compliance Item": "public/js/compliance_item.js",
	"Compliance Settings": "public/js/compliance_settings.js"
}

# override_doctype_dashboards = {}

# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
doctype_calendar_js = {
	"Contract": "public/js/contract_calendar.js",
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
	"Compliance Info": {
		"before_insert": "bloomstack_core.hook_events.compliance_info.create_bloomtrace_license",
	},
	"Compliance Settings": {
		"validate": "bloomstack_core.hook_events.compliance_settings.sync_bloomtrace"
	},
	"Delivery Note": {
		"before_submit": [
			"bloomstack_core.compliance.package.create_package_from_delivery"
		],
		"on_update_after_submit": "bloomstack_core.hook_events.delivery_note.link_invoice_against_delivery_note"
	},
	"Package Tag": {
		"validate": "bloomstack_core.hook_events.utils.create_integration_request",
		"after_insert": "bloomstack_core.hook_events.utils.create_integration_request"
	},
	"Stock Entry": {
		"on_submit": "bloomstack_core.compliance.package.create_package_from_stock"
	},
	"Delivery Trip": {
		"on_submit" : "bloomstack_core.hook_events.delivery_trip.make_transfer_templates",
	},
	"Item": {
		"on_update": "bloomstack_core.hook_events.utils.create_integration_request"
	},
	"Sales Invoice": {
		"before_submit": "bloomstack_core.hook_events.sales_invoice.create_metrc_sales_receipt"
	},
	"User": {
		"validate": [
			"bloomstack_core.hook_events.user.validate_if_bloomstack_user",
			"bloomstack_core.hook_events.user.update_bloomtrace_user"
		],
		"before_insert": "bloomstack_core.hook_events.user.set_works_with_bloomstack_false",
		"after_insert": "bloomstack_core.hook_events.user.update_bloomtrace_user"
	},
	"Plant Batch": {
		"on_update": "bloomstack_core.hook_events.plant_batch.create_integration_request"
	},
	"Plant": {
		"on_update": "bloomstack_core.hook_events.plant.create_integration_request"
	},
	"Strain": {
		"on_update": "bloomstack_core.hook_events.strain.create_integration_request"
	},
	"Plant Additive Log": {
		"on_update": "bloomstack_core.hook_events.plant_additive_log.create_integration_request"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"bloomstack_core.hook_events.user.execute_bloomtrace_integration_request",
		"bloomstack_core.hook_events.compliance_item.execute_bloomtrace_integration_request",
		"bloomstack_core.hook_events.package_tag.execute_bloomtrace_integration_request",
		"bloomstack_core.hook_events.delivery_note.execute_bloomtrace_integration_request",
		"bloomstack_core.hook_events.plant_batch.execute_bloomtrace_integration_request",
		"bloomstack_core.hook_events.plant.execute_bloomtrace_integration_request",
		"bloomstack_core.hook_events.strain.execute_bloomtrace_integration_request",
		"bloomstack_core.compliance.package.execute_bloomtrace_integration_request_for_stock_entry",
		"bloomstack_core.compliance.package.execute_bloomtrace_integration_request_for_delivery_note",
		"bloomstack_core.hook_events.plant_additive_log.execute_bloomtrace_integration_request"
	],
	"daily": [
		"bloomstack_core.hook_events.sales_order.create_sales_invoice_against_contract"
	],
	"daily_long": [
		"bloomstack_core.hook_events.sales_order.update_order_status"
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
