

import frappe


def before_pick_list_save(self):
	pass


def override_pick_list_validation(*args, **kwargs):
	# override the Pick List's validation trigger to prevent it from
	# re-calculating the item quantities based on batch locations
	# TODO: only keep until proper fix is made
	return

	# pick_list.PickList.before_save = before_pick_list_save
