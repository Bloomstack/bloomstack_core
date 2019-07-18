# -*- coding: utf-8 -*-
# Copyright (c) 2019, Bloom Stack and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe


def set_invoice_status(sales_invoice, method):
	sales_invoice.set_status()
	sales_invoice.set_indicator()