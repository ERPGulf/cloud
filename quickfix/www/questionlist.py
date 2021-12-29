import frappe
from quickfix.www.utils import paginate

# code for searching question in database

@frappe.whitelist(allow_guest=True)
def search_question(keyword):
    result= frappe.db.sql(f"""SELECT question_title,question_body FROM tabQuestions WHERE question_title OR question_body LIKE '%{keyword}%';""")
    return result

# code for displaying question in the page and pagination
def get_context(context):
    page=frappe.form_dict.page
    pagination=paginate(page)
    context.question=pagination.get('properties')
    context.prev=pagination.get('prev')
    context.next=pagination.get('next')
    
    return context
   