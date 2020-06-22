# -*- coding: utf-8 -*-777777yyy
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import csv
import sys
from frappe.utils import getdate, flt

def import_data():
	check_uom()
	print("UOM check complete.")
	make_items()
	print(" \nAR 2019 & Legacy Item Inserted.")
	check_fiscal_year()
	print(" \nFiscal Year check complete.")
	import_ar()
	print(" \nAR import complete.")
	import_invoices()
	print(" \nInvoice import complete.")
	apply_taxes()
	print(" \nApplying taxes complete.")
	submit_invoices()
	print(" \nAll invoices submitted sucessfully.")
	make_customer("AR Offset")
	print("Inserted Customer for AR Offset ")
	import_payments()
	print(" \nApplying payments complete.")
	import_non_standard_payments()
	print(" \nApplying non standard payments complete.")
	print(" \nData import was sucessful.")

def check_uom():
	uom = frappe.get_doc("UOM", 'Nos')
	uom.must_be_whole_number=False
	uom.save()

def make_items():
	autoname_item = frappe.db.get_single_value("Stock Settings", "autoname_item")
	if autoname_item:
		frappe.db.set_value("Stock Settings", "Stock Settings", "autoname_item", False)
	if not frappe.db.exists("Item", 'HF-OLD'):
		item = frappe.new_doc('Item')
		item.update({
			"name": "HF-OLD",
			"item_code": "HF-OLD",
			"item_name": "Legacy Item",
			"item_group": "All Item Groups",
			"stock_uom": "Nos",
			"is_stock_item": 0
		})
		item.save()
		frappe.db.commit()

	if not frappe.db.exists("Item", 'HF-AR-2019'):
		item = frappe.new_doc('Item')
		item.update({
			"name": "HF-AR-2019",
			"item_code": "HF-AR-2019",
			"item_name": "AR 2019",
			"item_group": "All Item Groups",
			"description": "AR Balance Carry forwarded from 2019 FY",
			"stock_uom": "Nos",
			"is_stock_item": 0
		})
		item.save()
		if autoname_item:
			frappe.db.set_value("Stock Settings", "Stock Settings", "autoname_item", True)

def check_fiscal_year():
	for fy in ['2018', '2019', '2020']:
		if not frappe.db.exists("Fiscal Year", fy):
			frappe.throw("Fiscal Year {0} not found".format(fy))

def import_ar():
	_file = frappe.get_doc("File", {"file_name": "AR.csv"})
	filename = _file.get_full_path()
	with open(filename, encoding='utf-8-sig') as csvfile:
		readCSV = csv.DictReader(csvfile)
		frappe.flags.in_import = True
		i = 1
		for row in readCSV:
			sys.stdout.write("\rImporting AR: Row {0}".format(i))
			sys.stdout.flush()
			i += 1
			customer = row["Customer"]
			if not customer:
				return
			if not frappe.db.exists("Customer", customer):
				make_customer(customer)
			if flt(row['Open Balance']) > 0:
				if not frappe.db.exists("Sales Invoice", row['Num']):
					make_ar_invoice(row)
			else:
				if not frappe.db.exists("Payment Entry", row['Num']):
					make_ar_payment_entry(row)
	frappe.db.commit()

def import_invoices():
	_file = frappe.get_doc("File", {"file_name": "invoices.csv"})
	filename = _file.get_full_path()
	with open(filename, encoding='utf-8-sig') as csvfile:
		readCSV = csv.DictReader(csvfile)
		frappe.flags.in_import = True
		i = 1
		for row in readCSV:
			sys.stdout.write("\rImporting Invoices: Row {0}".format(i))
			sys.stdout.flush()
			i += 1
			customer = row["Customer"]
			if not customer:
				return

			if not frappe.db.exists("Customer", customer):
				make_customer(customer)
			if not frappe.db.exists("Sales Invoice", row['Num']):
				make_invoice(row)
			else:
				update_invoice(row)
	frappe.db.commit()

def apply_taxes():
	_file = frappe.get_doc("File", {"file_name": "taxes.csv"})
	filename = _file.get_full_path()
	with open(filename, encoding='utf-8-sig') as csvfile:
		readCSV = csv.DictReader(csvfile)
		frappe.flags.in_import = True
		i = 1
		for row in readCSV:
			sys.stdout.write("\rApplying Taxes: Row {0}".format(i))
			sys.stdout.flush()
			i += 1
			if frappe.db.exists("Sales Invoice", row['Num']):
				apply_tax(row)
			else:
				print("Tax Not Applied")
	frappe.db.commit()

def submit_invoices():
	i = 1
	draft_invoices = frappe.get_all("Sales Invoice", filters={"docstatus":0})
	for invoice in draft_invoices:
		sys.stdout.write("\rSubmitting Invoice {0}".format(i))
		sys.stdout.flush()
		i += 1
		sales_invoice = frappe.get_doc("Sales Invoice", invoice.name)
		sales_invoice.submit()
	frappe.db.commit()

def import_payments():
	_file = frappe.get_doc("File", {"file_name": "payments.csv"})
	filename = _file.get_full_path()
	with open(filename, encoding='utf-8-sig') as csvfile:
		readCSV = csv.DictReader(csvfile)
		frappe.flags.in_import = True
		i = 1
		for row in readCSV:
			sys.stdout.write("\rApplying Payments: Row {0}".format(i))
			sys.stdout.flush()
			i += 1
			make_payment_entry(row)
	frappe.db.commit()

def import_non_standard_payments():
	_file = frappe.get_doc("File", {"file_name": "non_standard_payments.csv"})
	filename = _file.get_full_path()
	with open(filename, encoding='utf-8-sig') as csvfile:
		readCSV = csv.DictReader(csvfile)
		frappe.flags.in_import = True
		i = 1
		for row in readCSV:
			sys.stdout.write("\rApplying Non Standard Payments: Row {0}".format(i))
			sys.stdout.flush()
			i += 1
			make_journal_entries(row)
	frappe.db.commit()

def make_customer(customer_name):
	customer = frappe.new_doc("Customer")
	customer.update({
		"customer_name": customer_name,
		"type": "Company",
		"customer_group": "All Customer Groups",
		"territory": "All Territories"
	})
	customer.save()

def make_ar_invoice(row):
	invoice = frappe.new_doc("Sales Invoice")
	invoice.update({
		"name": row['Num'],
		"set_posting_time": 1,
		"posting_date": getdate(row['Date']),
		"customer": row['Customer'],
		"due_date":  getdate(row['Due Date']),
		"items": [{
			"item_code": "HF-AR-2019",
			"qty": 1,
			"rate": row['Open Balance']
		}]
	})
	invoice.insert()
	invoice.submit()

def make_ar_payment_entry(row):
	payment = frappe.new_doc("Payment Entry")
	amount = abs(flt(row['Open Balance']))
	payment.update({
		"name": row['Num'],
		"payment_type": "Receive",
		"posting_date": getdate(row['Date']),
		"party_type": "Customer",
		"party": row['Customer'],
		"received_amount": amount,
		"paid_amount": amount,
		"mode_of_payment": "Cash",
		"paid_to": "101100 - Cash - HF",
		"remarks": "AR Balance Carry forwarded from 2019 FY"
	})
	payment.insert()
	payment.submit()

def make_payment_entry(row):
	payment = frappe.new_doc("Payment Entry")
	amount = abs(flt(row['Amount']))
	mode_of_payment = "Cash"
	paid_to = "101100 - Cash - HF"

	if not frappe.db.exists("Customer", row['Customer']):
		make_customer(row['Customer'])

	if row['Split'] == "Coast Central *3090":
		mode_of_payment = "Bank Draft"
		paid_to = "102100 - Checking - Coast Central 3090 - HF"

	if row['Split'] == "Northern Redwood 6266":
		mode_of_payment = "Bank Draft"
		paid_to = "102120 - Checking - Northern Redwood 6266 - HF"

	payment.update({
		"payment_type": "Receive",
		"posting_date": getdate(row['Date']),
		"party_type": "Customer",
		"party": row['Customer'],
		"received_amount": amount,
		"paid_amount": amount,
		"mode_of_payment": mode_of_payment,
		"reference_date": getdate(row['Date']),
		"reference_no":  row['Num'],
		"paid_to": paid_to,
		"remarks": row['Num'] + ": " + row['Memo/Description']
	})
	if frappe.db.exists("Sales Invoice", row['Num']):
		allocated_amount =  frappe.db.get_value("Sales Invoice", row['Num'], "outstanding_amount")
		if allocated_amount > amount:
			allocated_amount = amount
		references = [{
			"reference_doctype": "Sales Invoice",
			"reference_name":  row['Num'],
			"allocated_amount": allocated_amount
		}]
		payment.update({
			"references": references
		})

	payment.insert()
	payment.submit()

def make_journal_entries(row):
	pass

def make_invoice(row):
	qty = flt(row['Qty'])
	if qty==0: qty=1
	invoice = frappe.new_doc("Sales Invoice")
	invoice.update({
		"name": row['Num'],
		"set_posting_time": 1,
		"posting_date": getdate(row['Date']),
		"customer": row['Customer'],
		"due_date":  getdate(row['Date']),
		"items": [{
			"item_code": "HF-OLD",
			"description": row['Product/Service'] + ": " + row['Memo/Description'],
			"qty": qty,
			"rate": row['Sales Price']
		}]
	})
	invoice.insert()

def update_invoice(row):
	qty = flt(row['Qty'])
	if qty==0: qty=1
	invoice = frappe.get_doc("Sales Invoice", row['Num'])
	items = invoice.items
	items.append({
		"item_code": "HF-OLD",
		"description": row['Product/Service'] + ": " + row['Memo/Description'],
		"qty": qty,
		"rate": row['Sales Price']
	})

	invoice.update({
		"items": items
	})
	invoice.save()

def apply_tax(row):
	invoice = frappe.get_doc("Sales Invoice", row['Num'])
	taxes = invoice.taxes
	if row['Product/Service'] == 'Cultivation Tax':
		tax = apply_cultivation_tax(row)
		taxes.append(tax)
	elif row['Product/Service'] == "CA Excise Tax (Arm's Length)":
		tax = apply_excise_tax(row)
		taxes.append(tax)

	invoice.update({
		"taxes": taxes
	})
	invoice.save()

def apply_cultivation_tax(row):
	return {
		'category': 'Total',
		'charge_type': 'Actual',
		'add_deduct_tax': 'Deduct',
		'description': row['Memo/Description'],
		'account_head': '203620 - Cultivation Tax Payable - Leaf - HF',
		'tax_amount': abs(flt(row['Amount']))
	}

def apply_excise_tax(row):
	return {
		'category': 'Total',
		'add_deduct_tax': 'Add',
		'charge_type': 'Actual',
		'description': row['Memo/Description'],
		'account_head': '203700 - Excise Tax Payable - HF',
		'tax_amount': row['Amount']
	}