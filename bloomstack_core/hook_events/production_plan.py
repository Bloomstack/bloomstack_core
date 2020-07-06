# -*- coding: utf-8 -*-
# Copyright (c) 2020, Bloomstack Inc. and contributors
# For license information, please see license.txt

import frappe

def set_workstations(doc, method):
	for item in doc.get("po_items"):
		bom_operations = frappe.get_all("BOM Operation", filters={"parent": item.bom_no}, fields=["workstation"])
		if bom_operations:
			workstations = [operation.workstation for operation in bom_operations if operation.workstation]
			item.workstations = '\n'.join(workstations)