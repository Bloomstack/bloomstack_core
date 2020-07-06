# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

import frappe

def set_workstations(doc, method):
	boms = frappe.get_all("BOM Operation" , fields=["*"])
	workstation_value = []
	for bom in doc.get("po_items"):
		for operation in boms:
			if operation.parent == bom.bom_no:
			   workstation_value.append(operation.workstation)
		bom.workstations = ', '.join(workstation_value)