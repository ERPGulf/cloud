import frappe

# code for pagination
def paginate(page=0):
    next,prev=0,0
    condition=" "
    query=""" SELECT question_title,question_body from tabQuestions ORDER BY creation DESC """
    if(page):
        page=int(page)
        properties=frappe.db.sql(query+f"""LIMIT {(page*4)-4},6;""",as_dict=True)
        next_set=frappe.db.sql(query+f"""LIMIT {page*4},6;""",as_dict=True)
        if(next_set):
            next,prev=page+1 ,page-1
        else:
            prev,next= page-1, 0
    else:
        count=frappe.db.sql(f"""SELECT COUNT(question_title) as count From tabQuestions;""",as_dict=True)[0].count
        if (count>4):
            prev,next=0,2
        else:
            pass
        properties=frappe.db.sql(query+""" LIMIT 6;""",as_dict=True)
    return {
        "properties" : properties,
        "prev" : prev,
        "next" : next
    }