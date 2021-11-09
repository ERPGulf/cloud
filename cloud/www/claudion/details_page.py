import frappe

# function to fetch the data based on selected instance
def get_context(context): 
    cloud= frappe.get_doc("Cloud",frappe.form_dict.name)
    context={
        "cloud":cloud
    }
    return context
    