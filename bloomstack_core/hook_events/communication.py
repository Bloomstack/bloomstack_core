import frappe 

def set_replied(doc, method):
    issue = frappe.get_doc("Issue", doc.reference_name)
    if doc.communication_type == "communication":
        if doc.recipients == issue.raised_by:
            issue.update({"status": "Replied"}).save()

        elif doc.sender == issue.raised_by:
            issue.update({"status": "Open"}).save()
