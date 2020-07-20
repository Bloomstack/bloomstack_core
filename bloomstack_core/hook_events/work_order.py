import frappe
from frappe.utils import now_datetime

@frappe.whitelist()
def start_job_cards(doctype, name):
	job_cards = []
	open_job_cards = frappe.db.get_all('Job Card', {
		'work_order':name, 'status':('in', ['Open', 'Work In Progress', 'Material Transferred'])
		}, ['*'])
	for job_card in open_job_cards:
		job = frappe.get_doc('Job Card', job_card.name)
		job.job_started = 1
		row = job.append('time_logs', {})
		row.from_time = now_datetime()
		row.completed_qty = 0
		job.save()
		job_cards.append(job.name)
	return job_cards
	

@frappe.whitelist()
def stop_job_cards(doctype, name):
	job_cards = []
	open_job_cards = frappe.db.get_all('Job Card', {
		'work_order':name, 'status':('in', ['Open', 'Work In Progress', 'Material Transferred'])
		}, ['*'])
	for job_card in open_job_cards:
		job = frappe.get_doc('Job Card', job_card.name)
		job.job_started = 0
		for row in job.time_logs:
			if not row.to_time:
				row.to_time = now_datetime()
				row.completed_qty = 0
				job_cards.append(row.parent)
		job.save()
	return job_cards

	
