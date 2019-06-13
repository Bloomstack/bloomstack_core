# -*- coding: utf-8 -*-
# Copyright(c) 2019, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _


def configure_system_settings(args):
	system_settings = frappe.get_single("System Settings")
	system_settings.float_precision = 2
	system_settings.currency_precision = 2
	system_settings.save()


def configure_selling_settings(args):
	selling_settings = frappe.get_single("Selling Settings")
	selling_settings.territory = None
	selling_settings.customer_group = None
	selling_settings.save()


def configure_stock_settings(args):
	# Avoid auto-selecting batches for state compliance
	stock_settings = frappe.get_single("Stock Settings")
	stock_settings.automatically_set_batch_nos_based_on_fifo = False
	stock_settings.save()


def disable_standard_reports(args):
	# Disable duplicate ERPNext address and contact report
	frappe.db.set_value("Report", "Addresses And Contacts", "disabled", 1)


def get_setup_stages(args=None):
	stages = [
		{
			'status': _('Configuring Bloomstack settings'),
			'fail_msg': _('Failed to configure Bloomstack settings'),
			'tasks': [
				{
					'fn': configure_system_settings,
					'args': args,
					'fail_msg': _("Failed to configure system settings")
				},
				{
					'fn': configure_selling_settings,
					'args': args,
					'fail_msg': _("Failed to configure selling settings")
				},
				{
					'fn': configure_stock_settings,
					'args': args,
					'fail_msg': _("Failed to configure stock settings")
				},
				{
					'fn': disable_standard_reports,
					'args': args,
					'fail_msg': _("Failed to disable standard reports")
				}
			]
		}
	]

	return stages
