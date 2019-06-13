import frappe
from erpnext.accounts.utils import get_balance_on


@frappe.whitelist()
def get_cash_in_hand_accounts():
	cash_in_hand_accounts = frappe.get_all("Account", filters={"is_cash_in_hand": 1})
	return {account.name: get_balance_on(account.name) for account in cash_in_hand_accounts}
