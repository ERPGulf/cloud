import frappe
from datetime import date,timedelta
import oci
import sys


#function to create a subscription document when a instance is created
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

# function to get the billing_intervell for the plan that give in the form
@frappe.whitelist(allow_guest=True)
def get_billing_intervell(value=None):
    plan = frappe.db.sql(f""" SELECT billing_interval FROM `tabSubscription Plan` WHERE plan_name ='{value}';""")
    return plan[0]


@frappe.whitelist(allow_guest=True)
def price_per_month(value=None):
    plan = frappe.db.sql(f""" SELECT cost FROM `tabSubscription Plan` WHERE plan_name ='{value}';""")
    return plan[0]

#fuction to get the username from db for the server booking form
@frappe.whitelist(allow_guest=True)
def get_username(uid):
    r = frappe.db.sql(f""" SELECT username FROM `tabUser` WHERE name ='{uid}';""")
    return r

# function to get the host_name from db 
@frappe.whitelist(allow_guest=True)
def get_host_name(uid):
    r = frappe.db.sql(f""" SELECT full_name FROM `tabUser` WHERE name ='{uid}';""")
    return r

#function to poweron the instance
@frappe.whitelist()    
def instance_poweron(current_oci_id):
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/cloud/doctype/cloud/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        }  
        try:
            core_client = oci.core.ComputeClient(config)
            # core_client.base_client.set_region('eu-frankfurt-1')
            id=current_oci_id
            # Send the request to service
            instance_action_response = core_client.instance_action(instance_id=id,action='START')
            return {"doNe"}
        except Exception as e:
            frappe.errprint(e.with_traceback())
            return {"error": True, "msg":e.with_traceback()}


#function for poweroff of the instance
@frappe.whitelist()    
def instance_poweroff(current_oci_id):
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/cloud/doctype/cloud/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        }  
        try:
            core_client = oci.core.ComputeClient(config)
            # core_client.base_client.set_region('eu-frankfurt-1')
            id=current_oci_id
            # Send the request to service
            instance_action_response = core_client.instance_action(instance_id=id,action='SOFTSTOP')
            return {"doNe"}
        except Exception as e:
            frappe.errprint(e.with_traceback())
            return {"error": True, "msg":e.with_traceback()}



#function to reboot the instance
@frappe.whitelist()    
def instance_reboot(current_oci_id):
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/cloud/doctype/cloud/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        }  
        try:
            core_client = oci.core.ComputeClient(config)
            # core_client.base_client.set_region('eu-frankfurt-1')
            id=current_oci_id
            # Send the request to service
            instance_action_response = core_client.instance_action(instance_id=id,action='SOFTRESET')
            return {"doNe"}
        except Exception as e:
            frappe.errprint(e.with_traceback())
            return {"error": True, "msg":e.with_traceback()}



#function to fetch the status of the instance
@frappe.whitelist() 
def intnc_stat(current_oci_id=None):   
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/cloud/doctype/cloud/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        }
        try:
            data=[]
            compute = oci.core.ComputeClient(config)
            compartment_id="ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq"
            instances=compute.list_instances(compartment_id).data
            for instance in instances:
                if (instance.id==current_oci_id):
                    json={instance.lifecycle_state}
                    return json
        except Exception as e:
            frappe.errprint(e.with_traceback())
            return {"error": True, "msg":e.with_traceback()}



#function to fetch the public_ip of the instance
@frappe.whitelist() 
def get_public_ip(current_oci_id=None): 
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/cloud/doctype/cloud/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        }
        try:
            compute_client = oci.core.ComputeClient(config)
            network_client = oci.core.VirtualNetworkClient(config)
            get_pub=oci.core.models.PublicIp()
            cd_compartment_id = config["tenancy"]
            instanceId = current_oci_id 
            vnic_id = compute_client.list_vnic_attachments(cd_compartment_id, instance_id=instanceId).data[0]
            private_ip = network_client.get_vnic(vnic_id.vnic_id).data
            json={private_ip.public_ip}
            return json
        except Exception as e:
            frappe.errprint(e.with_traceback())
            return {"error": True, "msg":e.with_traceback()}




#function to fetch the private_ip of the instance
@frappe.whitelist() 
def get_private_ip(current_oci_id=None):  
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/cloud/doctype/cloud/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        }
        try:
            compute_client = oci.core.ComputeClient(config)
            network_client = oci.core.VirtualNetworkClient(config)
            get_pub=oci.core.models.PublicIp()
            cd_compartment_id = config["tenancy"]
            instanceId = current_oci_id 
            vnic_id = compute_client.list_vnic_attachments(cd_compartment_id, instance_id=instanceId).data[0]
            private_ip = network_client.get_vnic(vnic_id.vnic_id).data
            json={private_ip.private_ip}
            return json
        except Exception as e:
            frappe.errprint(e.with_traceback())
            return {"error": True, "msg":e.with_traceback()}




