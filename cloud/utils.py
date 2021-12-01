import frappe
from datetime import date,timedelta
import oci
import sys
import pandas as pd
import oci
import frappe
from datetime import datetime,timedelta,timezone
import pytz


########functions of cloud doctype start############

#function to create a subscription document when a instance is created
def save_subscription(doc,event):

    ### adding the owner to the customer doctype if they are not in the customer doctype for permission ####

    owner=doc.owner                        #fetching the owner that is now creating a instance

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


###############functions of cloud doctype end#################



##############fuction of create instance webfprm start#############

# function to get the billing_intervell for the plan that give in the form
@frappe.whitelist(allow_guest=True)
def get_billing_intervell(value=None):
    plan = frappe.db.sql(f""" SELECT billing_interval FROM `tabSubscription Plan` WHERE plan_name ='{value}';""")
    return plan[0]


#function to get the cost per month
@frappe.whitelist(allow_guest=True)
def price_per_month(value=None):
    plan = frappe.db.sql(f""" SELECT cost FROM `tabSubscription Plan` WHERE plan_name ='{value}';""")
    return plan[0]

#fuction to get the username from db for the server booking form
@frappe.whitelist(allow_guest=True)
def get_username(uid):
    r = frappe.db.sql(f""" SELECT username FROM `tabUser` WHERE name ='{uid}';""")
    return r



# function to create compartment 
@frappe.whitelist()     
def create_compartment(user_name):  
            # Create a default configuration file 
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/cloud/doctype/cloud/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        } 

        try:
            # Initialize service client with default config file
            identity_client = oci.identity.IdentityClient(config)
            # Send the request to service with parameters
            create_compartment_response = identity_client.create_compartment(
                create_compartment_details=oci.identity.models.CreateCompartmentDetails(
                    compartment_id="ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
                    name=user_name,
                    description="test compartment"))

            # Get the data from response
            det=create_compartment_response.data
            return det.id
        except Exception as e:
            frappe.errprint(e.with_traceback())
            
            return {"error": True, "msg":e.with_traceback()  }


#function to create vcn
@frappe.whitelist()  
def create_vcn(current_cmp_id):
            # Create a default configuration file 
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/cloud/doctype/cloud/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        } 

        try:
            # Initialize service client with default config file
            core_client = oci.core.VirtualNetworkClient(config)
            # Send the request to service with parameters
            create_vcn_response = core_client.create_vcn(
                create_vcn_details=oci.core.models.CreateVcnDetails(
                    compartment_id=current_cmp_id,
                    cidr_blocks=["10.0.0.0/16"]
                    ))
            # Get the data from response
            det=create_vcn_response.data.id
            return det
        except Exception as e:
            frappe.errprint(e.with_traceback())
            
            return {"error": True, "msg":e.with_traceback()
             }


# fuction to save the compartment and vcn_id inside a doctype named comp_id
@frappe.whitelist() 
def save_cmp(ai,bi,user):
    comp_id=frappe.get_doc({
        "doctype":"comp_id",
        "combartment_id":ai,
        "vcn_id":bi,
        "user":user
    })
    comp_id.insert()
    frappe.db.commit()


#function to check if any compartment is created to the user
@frappe.whitelist()
def get_name(user_id):
    if frappe.db.exists("comp_id",user_id):
        return 1
    else:
        return 0
##############fuction of create instance webfprm end################





############function of details html page start############


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
def intnc_stat(current_oci_id,compartment_id):   
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
            compartment_id=compartment_id
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
def get_public_ip(current_oci_id,compartment_id): 
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
            cd_compartment_id = compartment_id
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
def get_private_ip(current_oci_id,compartment_id):  
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
            cd_compartment_id = compartment_id
            instanceId = current_oci_id 
            vnic_id = compute_client.list_vnic_attachments(cd_compartment_id, instance_id=instanceId).data[0]
            private_ip = network_client.get_vnic(vnic_id.vnic_id).data
            json={private_ip.private_ip}
            return json
        except Exception as e:
            frappe.errprint(e.with_traceback())
            return {"error": True, "msg":e.with_traceback()}


#function to get the graph
@frappe.whitelist(allow_guest=True)     
def metrics_graph():
    config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/cloud/doctype/cloud/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1"
    }
    try:
        t1="1h"

        id="ocid1.instance.oc1.me-jeddah-1.anvgkljr62vcruycxds6xla34ychb6zoc5gfw4c6un3ibtwkjxb42y5paofa"
            # Initialize service client with config file
        metric_client = oci.monitoring.MonitoringClient(config)
            # Request details for retrieving aggregated data
        metric_detail = oci.monitoring.models.SummarizeMetricsDataDetails()
            # Use query property to select metric('Memory Utilization') and provide the OCID of the instance as 'resourceId'
        q='MemoryUtilization[{0}]'.format(t1)
        metric_detail.query =q +'{resourceId=%s}.mean()'%id
            # Provide the start time and end time along with the resolution
        d= datetime.now(timezone.utc).isoformat()
        f=datetime.now(timezone.utc)-timedelta(hours=1)
        v=f.isoformat()
        metric_detail.start_time = v                                    
        metric_detail.end_time = d 
        metric_detail.resolution = "5m"
            # Give the namespace ane compartment id
        metric_detail.namespace = "oci_computeagent"
        compartment_id = "ocid1.compartment.oc1..aaaaaaaang6sa7iqgswc4b3rhcrr42pfywxdzqrub3x4avmpypt3o7zsumka"
            # Get the data from response
        details=(metric_client.summarize_metrics_data(compartment_id, metric_detail)).data[0]

        pts=details.aggregated_datapoints
        arr=[]
        arr1=[]
        for x in pts:
            y=x.value
            z=x.timestamp
            arr1.append(z)
            arr.append(y)
        # Use query property to select metric('CPU Utilization')
        q='CPUUtilization[{0}]'.format(t1)
        metric_detail.query =q +'{resourceId=%s}.mean()'%id
        # Get the data from response
        details=(metric_client.summarize_metrics_data(compartment_id, metric_detail)).data[0]
        pts=details.aggregated_datapoints
        arr3=[]
        for x in pts:
            y=x.value
            z=x.timestamp
            arr3.append(y)
        # Use query property to select metric('Disk IO Read')
        q='DiskIopsRead[{0}]'.format(t1)
        metric_detail.query =q +'{resourceId=%s}.rate()'%id
        # Get the data from response
        details=(metric_client.summarize_metrics_data(compartment_id, metric_detail)).data[0]
        pts=details.aggregated_datapoints
        arr4=[]
        for x in pts:
            y=x.value
            arr4.append(y)
        # Use query property to select metric('Disk IO Write')
        q='DiskIopsWritten[{0}]'.format(t1)
        metric_detail.query =q +'{resourceId=%s}.rate()'%id
        # Get the data from response
        details=(metric_client.summarize_metrics_data(compartment_id, metric_detail)).data[0]
        pts=details.aggregated_datapoints
        arr2=[]
        for x in pts:
            y=x.value
            arr2.append(y)
        # Use query property to select metric('Disk Bytes Write')
        q='DiskBytesWritten[{0}]'.format(t1)
        metric_detail.query =q +'{resourceId=%s}.rate()'%id
        # Get the data from response
        details=(metric_client.summarize_metrics_data(compartment_id, metric_detail)).data[0]
        pts=details.aggregated_datapoints
        arr5=[]
        for x in pts:
            y=x.value
            arr5.append(y)
        # Use query property to select metric('Disk Bytes Read')
        q='DiskBytesRead[{0}]'.format(t1)
        metric_detail.query =q +'{resourceId=%s}.rate()'%id
        # Get the data from response
        details=(metric_client.summarize_metrics_data(compartment_id, metric_detail)).data[0]
        pts=details.aggregated_datapoints
        arr6=[]
        for x in pts:
            y=x.value
            arr6.append(y)
        # Use query property to select metric('Network Recieve Bytes')
        q='NetworksBytesIn[{0}]'.format(t1)
        metric_detail.query =q +'{resourceId=%s}.rate()'%id
        # Get the data from response
        details=(metric_client.summarize_metrics_data(compartment_id, metric_detail)).data[0]
        pts=details.aggregated_datapoints
        arr7=[]
        for x in pts:
            y=x.value
            arr7.append(y)
        # Use query property to select metric('Network Transmit Bytes')
        q='NetworksBytesOut[{0}]'.format(t1)
        metric_detail.query =q +'{resourceId=%s}.rate()'%id
        # Get the data from response
        details=(metric_client.summarize_metrics_data(compartment_id, metric_detail)).data[0]
        pts=details.aggregated_datapoints
        arr8=[]
        for x in pts:
            y=x.value
            arr8.append(y)
        # Use query property to select metric('Load Average')
        q='LoadAverage[{0}]'.format(t1)
        metric_detail.query =q +'{resourceId=%s}.rate()'%id
        # Get the data from response
        details=(metric_client.summarize_metrics_data(compartment_id, metric_detail)).data[0]
        pts=details.aggregated_datapoints
        arr9=[]
        for x in pts:
            y=x.value
            arr9.append(y)
        # Use query property to select metric('Memory Allocation Stalls')
        q='MemoryAllocationStalls[{0}]'.format(t1)
        metric_detail.query =q +'{resourceId=%s}.rate()'%id
        # Get the data from response
        details=(metric_client.summarize_metrics_data(compartment_id, metric_detail)).data[0]
        pts=details.aggregated_datapoints
        arr10=[]
        for x in pts:
            y=x.value
            arr10.append(y)
        return {"time":arr1,"data":arr,"data1":arr3,"data2":arr4,"data3":arr2,"data4":arr5,"data5":arr6,"data6":arr7,"data7":arr8,"data8":arr9,"data9":arr10}
    except Exception as e:
        
            frappe.errprint(e.with_traceback())
            
            return {"error": True, "msg":e.with_traceback() }
 



 ############function of details html page end############






