from __future__ import unicode_literals
import frappe

def get_context(context):
	datas = frappe.db.sql(f""" SELECT * FROM `tabCloud`;""",as_dict=True)
	context = {
		"datas":datas
	}
	return context
