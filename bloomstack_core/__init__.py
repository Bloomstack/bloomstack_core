# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from erpnext.stock.doctype.pick_list.pick_list import PickList

__version__ = '0.0.1'


######################### Function Overrides #########################

# override the Pick List's validation trigger to prevent it from
# re-calculating the item quantities based on batch locations
# TODO: only keep until proper fix is made

def before_pick_list_save(self):
	pass


PickList.before_save = before_pick_list_save
