from __future__ import unicode_literals
import frappe


#function to fetch all the data stored in the cloud doctype from database
def get_context(context):
	datas = frappe.db.sql(f""" SELECT * FROM `tabCloud`;""",as_dict=True)
	context = {
		"datas":datas,
	}
	return context



