from __future__ import unicode_literals

import frappe
from frappe.utils import cint

@frappe.whitelist()
def search(text, start=0, limit=10):

    # This could be changed to text matching instead of strictly searching doc names
    sql = """
    WITH search AS (
        SELECT * FROM (
            SELECT 'Serial No' as doctype, name as docname, serial_no as searchfield FROM `tabSerial No`
            UNION
            SELECT 'Batch' as doctype, name as docname, concat(batch_id, '.', package_tag) as searchfield FROM `tabBatch`
            UNION
            SELECT parenttype as doctype, parent as docname, package_tag as searchfield FROM `tabStock Entry Detail`
        ) q
        WHERE
            q.docname LIKE %(text)s OR q.searchfield LIKE %(text)s
    )
    SELECT
        doctype,
        docname,
        (SELECT COUNT(0) FROM search) as total_rows
    FROM search
    ORDER BY
        docname ASC
    LIMIT
        %(start)s, %(limit)s;
    """

    results = frappe.db.sql(sql, {
        "text": "%" + text + "%",
        "start": cint(start),
        "limit": cint(limit)
    }, as_list=1, debug=1)

    return results
