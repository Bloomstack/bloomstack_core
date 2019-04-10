import frappe


def boot_session(bootinfo):
	bootinfo.user.background_image = "/assets/bloomstack_core/images/desk.png"
	bootinfo.growth_guide_link = frappe.db.get_single_value("Bloomstack Settings", "growth_guide_link")