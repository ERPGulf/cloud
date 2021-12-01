import frappe
import oci
from frappe.model.document import Document
from datetime import datetime,timedelta

# function to create an indtance
@frappe.whitelist()     
def instnc_create(name,cmp_id,sub_id): 
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/cloud/doctype/cloud/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        }   
        try:
            core_client = oci.core.ComputeClient(config)
            launch_instance_response = core_client.launch_instance(
                launch_instance_details=oci.core.models.LaunchInstanceDetails(
                     display_name=name,
                     availability_domain="hhCz:ME-JEDDAH-1-AD-1",
                     compartment_id=cmp_id,
                     shape="VM.Standard.A1.Flex",
                     subnet_id=sub_id,
                     image_id="ocid1.image.oc1.me-jeddah-1.aaaaaaaadr6nyayryqfg65zijjxk7ztecorskuv4zhg6w52stvdx5uavm3aa",
                     shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
                         ocpus=1.0,
                         memory_in_gbs=1.0),
                         )
                         )
            instance=launch_instance_response.data
            json =  instance.id
            return json
        except Exception as e:
            frappe.errprint(e.with_traceback())
            print(instance)
            return {"error": True, "msg":e.with_traceback() }


#function to create subnet
@frappe.whitelist(allow_guest=True)    
def create_subnet(comp,vcn,s_name):  
            # Create a default configuration file
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/cloud/doctype/cloud/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        }
        try:
            core_client = oci.core.VirtualNetworkClient(config)
            value = frappe.db.get_value('cidrr','cidrr', 'block')
            value=int(value)+1
            x=frappe.client.set_value('cidrr','cidrr', 'block',value)
            y=x.block
            create_subnet_response = core_client.create_subnet(
            create_subnet_details=oci.core.models.CreateSubnetDetails(
                cidr_block="10.0.{}.0/24".format(y),
                compartment_id=comp,
                vcn_id=vcn,
                display_name=s_name,
                prohibit_internet_ingress=False,
                prohibit_public_ip_on_vnic=False
                ))
            det =create_subnet_response.data.id
            return det
        except Exception as e:
            frappe.errprint(e.with_traceback())
            return {"error": True, "msg":e.with_traceback() }



class Cloud(Document):
    # setting day until due for the subscription list billing intervell fetch from the plann doctype
    def before_insert(self):
        if(self.billing_intervell=="Day"):
            self.day_until_due=1                #function to get the billing intervel of the plan for subscription doctype
        if(self.billing_intervell=="Week"):
            self.day_until_due=7
        if(self.billing_intervell=="Month"):
            self.day_until_due=31
        if(self.billing_intervell=="Year"):
            self.day_until_due=365

        # setting the trial period start date and end date based on user choice
        if(self.need_one_month_trail==1):             # cheking if the user want a trial period
            start_date=datetime.today()               # setting the start date as today date
            end_date=start_date+timedelta(days=30)    #setting the end date
            self.trail_period_start_date=start_date
            self.trail_period_end_date=end_date

       

        

        current_user=frappe.session.user #code to find the current logined user
        comp=frappe.db.get_value('comp_id', current_user, 'combartment_id') #fetching compartment_id from comp_id doctype
        self.compartment_id=comp 
        vcn=frappe.db.get_value('comp_id', current_user, 'vcn_id') #fetching vcn_id from comp_id doctype
        self.vcn_id=vcn
        #calling the fuction to create subnet inside the vcn that is created
        subnet=create_subnet(comp,vcn,self.label)
        self.subnet_id=subnet

        # calling the function to create the instance in cloud
        data=instnc_create(self.label,comp,subnet)
        self.oci = data



        
        
        

       
    
