"""
Configuration for docs
"""

import frappe

# source_link = "https://github.com/[org_name]/bloomstack_core"
# docs_base_url = "https://[org_name].github.io/bloomstack_core"
# headline = "App that does everything"
# sub_heading = "Yes, you got that right the first time, everything"


def get_context(context):
	context.brand_html = "Bloomstack Core"


@frappe.whitelist()
def get_growth_guide_articles(doc_type):
	articles = frappe.db.sql("""
		SELECT
			article.name,
			article.route
		FROM
			`tabGrowth Guide Article` AS article
				JOIN `tabGrowth Guide Article Reference` AS ref
					ON ref.parent = article.name
		WHERE
			ref.doc_type = %s
	""", (doc_type), as_dict=1)

	return articles