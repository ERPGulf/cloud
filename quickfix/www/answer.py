import frappe


# code for getting answer typed by a user

@frappe.whitelist(allow_guest=True)

def insert_answer(answer,title):
    doc = frappe.get_doc('Questions', title)
    doc.append('answer', {'answer': answer})
    doc.save(ignore_permissions=True)

# code for getting previously entered answers

@frappe.whitelist(allow_guest=True)
def get_answers(title):
    
    answer=frappe.db.sql('select answer from tabAnswer where parent="%s"'%title,as_dict=True)
    return answer

# code for fetching question body

@frappe.whitelist(allow_guest=True)
def get_questionbody(title):
    body=frappe.db.sql('select question_body from tabQuestions where question_title="%s"'%title)
    return body
    

