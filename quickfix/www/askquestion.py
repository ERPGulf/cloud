import frappe

# code for inserting question to doc
@frappe.whitelist(allow_guest=True)
def insert_question(title,body):
    todo = frappe.get_doc({"doctype":"Questions", "question_title": title,"question_body":body})
    todo.insert(ignore_permissions=True)
    
