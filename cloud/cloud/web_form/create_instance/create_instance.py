from __future__ import unicode_literals
import frappe

def get_context(context):
	datas = frappe.db.sql(f""" SELECT * FROM `tabCloud`;""",as_dict=True)
	regions=frappe.db.sql(f"""SELECT * FROM `tabRegion`;""",as_dict=True)
	plans=frappe.db.sql(f"""SELECT * FROM `tabSubscription Plan`;""",as_dict=True)
	distributions=frappe.db.sql(f"""SELECT * FROM `tabDistributions`;""",as_dict=True)

	

	context = {
		"datas":datas,
		"regions":regions,
		"plans":plans,
		"distributions":distributions
	}
	return context
