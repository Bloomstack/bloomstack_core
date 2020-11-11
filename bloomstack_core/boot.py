import frappe


def boot_session(bootinfo):
	bootinfo.user.background_image = "/assets/bloomstack_core/images/desk.png"

	if frappe.conf.staging_server:
		bootinfo.staging_server = True
