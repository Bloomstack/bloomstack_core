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
	"/assets/bloomstack_core/js/query_report.js"
]
app_include_css = [
	"/assets/bloomstack_core/css/buttons.css",
	"/assets/bloomstack_core/css/trees.css",
	"/assets/bloomstack_core/css/mobile-fixes.css"
]

# include js, css files in header of web template
web_include_css = [
	"/assets/bloomstack_core/css/buttons.css"
]
# web_include_js = "/assets/bloomstack_core/js/bloomstack_core.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"User": "public/js/user.js",
	"Customer": "public/js/customer.js",
	"Company": "public/js/company.js",
	"Supplier": "public/js/supplier.js",
	"Item": "public/js/item.js",
	"Batch": "public/js/batch.js",
	"Quotation": "public/js/quotation.js",
	"Contract": "public/js/contract.js",
	"Delivery Trip": "public/js/delivery_trip.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
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

# notification_config = "bloomstack_core.notifications.get_notification_config"

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
	"Item": {
		"autoname": "bloomstack_core.hook_events.item.autoname"
	},
	"Purchase Receipt": {
		"on_submit": "bloomstack_core.hook_events.purchase_receipt.set_package_tags"
	},
	"Stock Entry": {
		"on_submit": "bloomstack_core.compliance.package.create_package"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"bloomstack_core.tasks.all"
# 	],
# 	"daily": [
# 		"bloomstack_core.tasks.daily"
# 	],
# 	"hourly": [
# 		"bloomstack_core.tasks.hourly"
# 	],
# 	"weekly": [
# 		"bloomstack_core.tasks.weekly"
# 	]
# 	"monthly": [
# 		"bloomstack_core.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "bloomstack_core.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "bloomstack_core.event.get_events"
# }
