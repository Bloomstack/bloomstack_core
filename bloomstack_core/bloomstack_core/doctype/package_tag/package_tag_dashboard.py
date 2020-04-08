from __future__ import unicode_literals

from frappe import _


def get_data():
	return {
		'fieldname': 'package_tag',
		'transactions': [
			{
				'label': _('Buy'),
				'items': ['Purchase Invoice', 'Purchase Receipt']
			},
			{
				'label': _('Sell'),
				'items': ['Sales Invoice', 'Delivery Note']
			},
			{
				'label': _('Move'),
				'items': ['Stock Entry']
			},
			{
				'label': _('Quality'),
				'items': ['Quality Inspection']
			}
		]
	}
