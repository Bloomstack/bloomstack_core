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

# Set session defaults
override_document_validations = [
	"bloomstack_core.session.override_pick_list_validation"
]

update_website_context = override_document_validations
on_session_creation = override_document_validations
on_login = override_document_validations

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_js = [
	"/assets/bloomstack_core/js/conf.js",
	"/assets/bloomstack_core/js/query_report.js",
	"/assets/bloomstack_core/js/banner.js",
	"/assets/bloomstack_core/js/utils.js",
	"/assets/js/address_and_contact.min.js"
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
	"Contract": "public/js/contract.js",
	"Delivery Note": "public/js/delivery_note.js",
	"Delivery Trip": "public/js/delivery_trip.js",
	"Driver": "public/js/driver.js",
	"Item": "public/js/item.js",
	"Lead": "public/js/lead.js",
	"Packing Slip": "public/js/packing_slip.js",
	"Pick List": "public/js/pick_list.js",
	"Project": "public/js/project.js",
	"Quality Inspection": "public/js/quality_inspection.js",
	"Quotation": "public/js/quotation.js",
	"Sales Order": "public/js/sales_order.js",
	"Task": "public/js/task.js",
	"Timesheet": "public/js/timesheet.js",
	"User": "public/js/user.js",
	"Work Order": "public/js/work_order.js"
}

doctype_list_js = {
	"Delivery Trip": "public/js/delivery_trip_list.js",
	"Sales Order": "public/js/sales_order_list.js",
	"Sales Invoice": "public/js/sales_invoice_list.js",
	"Purchase Order": "public/js/purchase_order_list.js",
	"Purchase Invoice": "public/js/purchase_invoice_list.js"
}

override_doctype_dashboards = {
	"Contract": "bloomstack_core.hook_events.contract.get_data",
	"Employee": "bloomstack_core.hook_events.employee.get_data",
	"Item": "bloomstack_core.hook_events.item.get_data",
}

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
	"Contract": {
		"validate": "bloomstack_core.hook_events.contract.generate_contract_terms_display",
		"on_update_after_submit": [
			"bloomstack_core.hook_events.contract.create_project_against_contract",
			"bloomstack_core.hook_events.contract.create_order_against_contract"
		]
	},
	"Customer": {
		"validate": [
			"bloomstack_core.hook_events.customer.update_lead_acc_open_date"
		]
	},
	("Company", "Supplier", "Customer"): {
		"validate": [
			"bloomstack_core.hook_events.utils.validate_default_license",
			"bloomstack_core.hook_events.utils.validate_expired_licenses"
		]
	},
	"Delivery Note": {
		"validate": "bloomstack_core.hook_events.delivery_note.link_invoice_against_delivery_note",
		"before_submit": [
			"bloomstack_core.hook_events.delivery_note.make_sales_invoice_for_delivery",
			"bloomstack_core.hook_events.delivery_note.link_invoice_against_delivery_note"
		]
	},
	"Sales Order": {
		"validate": "bloomstack_core.hook_events.sales_order.validate_batch_item"
	},
	"Delivery Trip": {
		"validate": [
			"bloomstack_core.hook_events.delivery_trip.generate_directions_url",
			"bloomstack_core.hook_events.delivery_trip.link_invoice_against_trip"
		],
		"on_update_after_submit": "bloomstack_core.hook_events.delivery_trip.set_vehicle_last_odometer_value",
	},
	"Driver": {
		"validate": "bloomstack_core.hook_events.driver.get_employee_from_user"
	},
	"Employee": {
		"validate": "bloomstack_core.hook_events.employee.update_driver_employee"
	},
	"Item": {
		"autoname": "bloomstack_core.hook_events.item.autoname"
	},
	"Packing Slip": {
		"on_submit": "bloomstack_core.hook_events.packing_slip.create_stock_entry"
	},
	"Pick List": {
		"on_submit": [
			"bloomstack_core.hook_events.pick_list.update_order_package_tag",
			"bloomstack_core.hook_events.pick_list.update_package_tag"
		],
		"before_submit" :[
			"bloomstack_core.hook_events.pick_list.set_picked_qty"
		],
		"on_cancel": [
			"bloomstack_core.hook_events.pick_list.update_order_package_tag",
			"bloomstack_core.hook_events.pick_list.update_package_tag"
		]
	},
	"Purchase Receipt": {
		"before_submit": "bloomstack_core.hook_events.purchase_receipt.create_package_tag",
		"on_submit": "bloomstack_core.hook_events.purchase_receipt.update_package_tags",
		# ERPNext tries to delete auto-created batches on cancel, so removing the link
		# from Package Tag before the on_cancel hook runs
		"before_cancel": "bloomstack_core.hook_events.purchase_receipt.update_package_tags"
	},
	"Sales Invoice": {
		"before_update_after_submit": "bloomstack_core.hook_events.sales_invoice.set_invoice_status"
	},
	"Stock Entry": {
		"on_submit": "bloomstack_core.compliance.package.create_package"
	},
	"User": {
		"validate": [
			"bloomstack_core.hook_events.user.validate_if_bloomstack_user",
			"bloomstack_core.hook_events.user.update_bloomtrace_user"
		],
		"before_insert": "bloomstack_core.hook_events.user.set_works_with_bloomstack_false",
		"after_insert": "bloomstack_core.hook_events.user.update_bloomtrace_user"
	},
	('Quotation', 'Sales Invoice', 'Sales Order', 'Delivery Note', 'Supplier Quotation', 'Purchase Invoice', 'Purchase Order', 'Purchase Receipt'): {
		'validate': [
			'bloomstack_core.hook_events.utils.validate_license_expiry',
			'bloomstack_core.hook_events.taxes.calculate_cannabis_tax'
		]
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"bloomstack_core.hook_events.sales_order.create_sales_invoice_against_contract"
	],
	"all": [
		"bloomstack_core.hook_events.user.execute_bloomtrace_integration_request",
		"bloomstack_core.hook_events.compliance_item.execute_bloomtrace_integration_request"
	]
}

after_migrate = ['bloomstack_core.hook_events.lead.rearrange_standard_fields']

# Testing
# -------

# before_tests = "bloomstack_core.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------

override_whitelisted_methods = {
	"erpnext.selling.doctype.sales_order.sales_order.create_pick_list": "bloomstack_core.hook_events.pick_list.create_pick_list"
}
