import frappe
from datetime import date,timedelta


def save_subscription(doc,event):

    ### adding the owner to the customer doctype if they are not in the customer doctype for permission ####

    owner=doc.owner                        #fetching the owner that is now creating a linode

    customer=frappe.db.sql(f"""select name from `tabCustomer`;""",as_dict=True) #fetching all the customer in the customer table in the system
    coustomer_list=[d['name'] for d in customer]   #converting that list of dictionary to  a single list
    if(owner in coustomer_list):          #cheking if the owner is in the customer list if yes pass
        pass
    else:
        add_customer=frappe.get_doc({     #if the owner not in the customer list add the owner to the customer doctype
            "doctype":"Customer",
            "customer_name":owner
        })
        add_customer.insert()
        frappe.db.commit()

    #### end of adding to customer doctype####


    day_until_due=doc.day_until_due                     #fetching day_until_due from the doc

    today_date=date.today()                             #initialising todays date
    End_date=today_date+timedelta(days=30)              # setting the end date of the trail period 
    sub_start=End_date+timedelta(days=1)                #setting the subscription start date when there is trial period enabled
    sub_end=sub_start+timedelta(days=day_until_due)     #setting the subscription end date when trail period is enabled       

    subscription_end_date=today_date+timedelta(days=day_until_due) #subscription end date when there is no trial period

    
    plans=doc.plan                      #fetching the paln doc from the form
    quantity_Of_plan=doc.quantity       #quantity of the plane
    
    
    if(doc.need_one_month_trail==True):
        note=frappe.get_doc({
        "doctype":"Subscription",
        "party_type":"Customer",      # dynamically adding the values to the subscription doctype if there is trial period enabled
        "party":owner,
        "trial_period_start":today_date,
        "trial_period_end":End_date,
        "start_date":sub_start,
        "end_date":sub_end,
        "days_until_due":day_until_due
        })
        note.append("plans",{
        "plan":plans,            #adding the plane and quandity to the child table inside the subscription doctype
        "qty":quantity_Of_plan
        })
        note.insert()  #inserting in to the doctype
        frappe.db.commit()
    else:
        note=frappe.get_doc({
        "doctype":"Subscription",
        "party_type":"Customer",      # dynamically adding the values to the subscription doctype is there is no trial period
        "party":owner,
        "start_date":today_date,
        "end_date":subscription_end_date,
        "days_until_due":day_until_due
        })
        note.append("plans",{
        "plan":plans,            #adding the plane and quandity to the child table inside the subscription doctype
        "qty":quantity_Of_plan
        })
        note.insert()  #inserting in to the doctype
        frappe.db.commit()