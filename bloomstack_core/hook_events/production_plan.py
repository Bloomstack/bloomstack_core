# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.utils import get_url, cstr
from urllib.parse import urlparse

def set_workstations(doc, method):
    boms = frappe.get_all("BOM Operation" , fields=["*"])
    for bom in doc.get("po_items"):
        operations =  next((data for data in boms if data.get("parent") == bom.get("bom_no")), None)
        if not operations:
            continue
        bom.workstations = operations.workstation
