from __future__ import unicode_literals
import frappe

from frappe.model.document import Document
import oci
import sys

#function to view inbound rules
@frappe.whitelist()     
def security_list_view():  
            # Create a default configuration file 
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/www/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        } 

        try:
             # Initialize service client with config file
            core_client = oci.core.VirtualNetworkClient(config)
            identity_client = oci.identity.IdentityClient(config)
            # Provide details of the security list to be viewed
            compartment_id="ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq"
            vcn_id="ocid1.vcn.oc1.me-jeddah-1.amaaaaaa62vcruya5myc3mreogctutotajwahpjepv3bim3dazwxac2jtrya"
            subnet_id="ocid1.subnet.oc1.me-jeddah-1.aaaaaaaawmnhlihg6euaspjqvkkhgb24tirpi5dhkhme47rk6c77fhfxl4ha"
            seclist_name="Default Security List for Hiba-test-subnet"
            # Send request to service with the required parameters
            list_security_lists_response = core_client.list_security_lists(
                compartment_id=compartment_id,
                display_name=seclist_name,
                sort_order="DESC")
            # Get the data from response 
            
            current_security_list = list_security_lists_response.data[0]
            
            # List the security rules available by looping through the data
            ingress_ruless=[]
            if len(current_security_list.ingress_security_rules) > 0:
                for il in current_security_list.ingress_security_rules:
                    if(il.protocol=="6"):
                        if(il.tcp_options==None):
                                json={"description":il.description,"source":il.source,"protocol":il.protocol,"port_min":"","port_max":""}
                                ingress_ruless.append(json)
                                continue
                        else:
                                port=il.tcp_options.destination_port_range
                                json={"description":il.description,"source":il.source,"protocol":il.protocol,"port_min":port.min,"port_max":port.max}
                                ingress_ruless.append(json)
                                continue
               
                    if(il.protocol=="17"):
                        if(il.udp_options==None):
                                json1={"description":il.description,"source":il.source,"protocol":il.protocol,"port_min":"","port_max":""}
                                ingress_ruless.append(json1)
                                continue
                        
                        else:
                                port1=il.udp_options.destination_port_range
                                json1={"description":il.description,"source":il.source,"protocol":il.protocol,"port_min":port1.min,"port_max":port1.max}
                                ingress_ruless.append(json1)
                                continue
                    if(il.protocol=="all"):
                        json3={"description":il.description,"source":il.source,"protocol":il.protocol,"port_min":"","port_max":""}
                        ingress_ruless.append(json3)
                        continue

                    else:
                        port2=il.icmp_options
                        if(port2==None):
                            json2={"description":il.description,"source":il.source,"protocol":il.protocol,"port_min":"","port_max":""}
                            ingress_ruless.append(json2)
                            continue
                        elif(port2.code==None):
                            json2={"description":il.description,"source":il.source,"protocol":il.protocol,"port_min":"","port_max":port2.type}
                            ingress_ruless.append(json2)
                            continue
                        elif(port2.type==""):
                            json2={"description":il.description,"source":il.source,"protocol":il.protocol,"port_min":"","port_max":port2.code}
                            ingress_ruless.append(json2)
                            continue

                        else:
                             json2={"description":il.description,"source":il.source,"protocol":il.protocol,"port_min":port2.code,"port_max":port2.type}
                             ingress_ruless.append(json2)
                             continue
                       
                       

            return ingress_ruless
        except Exception as e:
            frappe.errprint(e.with_traceback())
            
            return {"error": True, "msg":e.with_traceback() }



#function to view outbound rules
@frappe.whitelist()     
def egress_rules_list_view():  
            # Create a default configuration file 
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/www/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        } 

        try:
            # Initialize service client with config file
            core_client = oci.core.VirtualNetworkClient(config)
            identity_client = oci.identity.IdentityClient(config)
            # Provide details of the security list to be viewed
            compartment_id="ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq"
            vcn_id="ocid1.vcn.oc1.me-jeddah-1.amaaaaaa62vcruya5myc3mreogctutotajwahpjepv3bim3dazwxac2jtrya"
            subnet_id="ocid1.subnet.oc1.me-jeddah-1.aaaaaaaawmnhlihg6euaspjqvkkhgb24tirpi5dhkhme47rk6c77fhfxl4ha"
            seclist_name="Default Security List for Hiba-test-subnet"
            name = sys.argv[0]
            # Send request to service with the required parameters
            list_security_lists_response = core_client.list_security_lists(
               compartment_id=compartment_id,
               display_name=seclist_name,
               sort_order="DESC")
            current_security_list = list_security_lists_response.data[0]
            egress_ruless=[]
            # List the security rules available by looping through the data
            if len(current_security_list.egress_security_rules) > 0:
                for il in current_security_list.egress_security_rules:
                    

                    if(il.protocol=="6"):
                        if(il.tcp_options==None):
                            json={"description":il.description,"destination":il.destination,"protocol": il.protocol,"port_min":"","port_max":""}
                            egress_ruless.append(json)
                            continue
                        else:
                            port=il.tcp_options.destination_port_range
                            
                            json={"description":il.description,"destination":il.destination,"protocol": il.protocol,"port_min":port.min,"port_max":port.max}
                            egress_ruless.append(json)
                            continue
               
                    if(il.protocol=="17"):
                        if(il.udp_options==None):
                            json1={"description":il.description,"destination":il.destination,"protocol": il.protocol,"port_min":"","port_max":""}
                            egress_ruless.append(json1)
                            continue
                        else:
                            port1=il.udp_options.destination_port_range
                            json1={"description":il.description,"destination":il.destination,"protocol":il.protocol,"port_min":port1.min,"port_max":port1.max}
                            egress_ruless.append(json1)
                            continue

                    if(il.protocol=="1"):
                        port2=il.icmp_options
                        if(il.icmp_options==None):
                            json2={"description":il.description,"destination":il.destination,"protocol": il.protocol,"port_min":"","port_max":""}
                            egress_ruless.append(json2)
                            continue
                        elif(port2.code==""):
                            port2=il.icmp_options
                            json2={"description":il.description,"destination":il.destination,"protocol": il.protocol,"port_min":port2.type,"port_max":""}
                            egress_ruless.append(json2)
                            continue
                        elif(port2.type==""):
                            port2=il.icmp_options
                            json4={"description":il.description,"destination":il.destination,"protocol": il.protocol,"port_min":"","port_max":port2.code}
                            egress_ruless.append(json4)
                            continue
                        else:
                            port2=il.icmp_options
                            json2={"description":il.description,"destination":il.destination,"protocol": il.protocol,"port_min":port2.type,"port_max":port2.code}
                            egress_ruless.append(json2)
                            continue
                        
                    if(il.protocol=="58"):
                    
                        if(il.icmp_options==None):
                            json3={"description":il.description,"destination":il.destination,"protocol": il.protocol,"port_min":"","port_max":""}
                            egress_ruless.append(json3)
                            continue
                        elif(port2.code==""):
                            port2=il.icmp_options
                            json3={"description":il.description,"destination":il.destination,"protocol": il.protocol,"port_min":port2.type,"port_max":""}
                            egress_ruless.append(json3)
                            continue
                        elif(port2.type==""):
                            port2=il.icmp_options
                            json3={"description":il.description,"destination":il.destination,"protocol": il.protocol,"port_min":"","port_max":port2.code}
                            egress_ruless.append(json3)
                            continue
                        else:
                            port2=il.icmp_options
                            json3={"description":il.description,"destination":il.destination,"protocol": il.protocol,"port_min":port2.type,"port_max":port2.code}
                            egress_ruless.append(json3)
                            continue
                        
                    else:
                        port3=il.icmp_options
                        json4={"description":il.description,"destination":il.destination,"protocol":il.protocol,"port_max":" ","port_min":" "}
                        egress_ruless.append(json4)
                        continue
            return egress_ruless
        except Exception as e:
            frappe.errprint(e.with_traceback())
            return {"error": True, "msg":e.with_traceback() }



#function to delete inbound rules
@frappe.whitelist(allow_guest=True)
def delete_ingress_rule(descriptionn,protocoll,port_minn,port_maxx,sourcee):
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/www/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        }
        
        try:
            #  Initialize service client with config file
            
            core_client = oci.core.VirtualNetworkClient(config)
            identity_client = oci.identity.IdentityClient(config)
            # Provide details of security list 
            compartment_id="ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq"
            vcn_id="ocid1.vcn.oc1.me-jeddah-1.amaaaaaa62vcruya5myc3mreogctutotajwahpjepv3bim3dazwxac2jtrya"
            subnet_id="ocid1.subnet.oc1.me-jeddah-1.aaaaaaaawmnhlihg6euaspjqvkkhgb24tirpi5dhkhme47rk6c77fhfxl4ha"
            seclist_name="Default Security List for Hiba-test-subnet"
            name = sys.argv[0]
            desc=descriptionn
            pmax=port_maxx
            if(desc==""):
                desc=" "
            if (desc=='None'):
                desc=None
            else:
                desc=descriptionn
                
            if(port_maxx=='None'):
                pmax=None
            elif((port_maxx=="")|(port_maxx==" ")): 
                pmax=None
               
            else:
                pmax=int(port_maxx)
            pmin=port_minn
            if(pmin=='None'):
                pmin=None
            elif((port_minn=="")|(port_minn==" ")): 
                pmin=None
            else:
                pmin=int(port_minn)
            
            if len(sys.argv) >= 3:
                new_ip = sys.argv[2]
            else:
                new_ip = None
            # List the rules available in the security list
            list_security_lists_response = core_client.list_security_lists(
                compartment_id=compartment_id,
                display_name=seclist_name,
                sort_order="DESC")
            current_security_list = list_security_lists_response.data[0]
            # Add them to a list named new_ingress_security_list
            new_ingress_security_rules = []
            found_name = False
            if len(current_security_list.ingress_security_rules) > 0:
                for il in current_security_list.ingress_security_rules:
                    if il.description == name:
                        found_name = True
                        
                        if new_ip != None:
                            il.source = new_ip+'/32'
                            new_ingress_security_rules.append(il)
                    else:
                        new_ingress_security_rules.append(il)
            # Provide details of security rule to be deleted
            if(protocoll=='6'):
                if(pmax==None):
                    ingress_security_rules=[oci.core.models.IngressSecurityRule(
                    description=desc,protocol=protocoll,
                    source=sourcee,
                    is_stateless=False,
                    source_type="CIDR_BLOCK",
                    tcp_options=None)]
                else:
                    ingress_security_rules=[oci.core.models.IngressSecurityRule(
                    description=desc,protocol=protocoll,
                    source=sourcee,
                    is_stateless=False,
                    source_type="CIDR_BLOCK",
                    tcp_options=oci.core.models.TcpOptions(
                        destination_port_range=oci.core.models.PortRange(
                            max=pmax,
                            min=pmin))
                            )]
                
            elif(protocoll=="17"):
                if(pmax==None):
                    ingress_security_rules=[oci.core.models.IngressSecurityRule(
                    description=desc,protocol=protocoll,
                    source=sourcee,
                    is_stateless=False,
                    source_type="CIDR_BLOCK",
                    udp_options=None)]
                else:
                    ingress_security_rules=[oci.core.models.IngressSecurityRule(
                    description=desc,protocol=protocoll,
                    source=sourcee,
                    is_stateless=False,
                    source_type="CIDR_BLOCK",
                    udp_options=oci.core.models.UdpOptions(
                        destination_port_range=oci.core.models.PortRange(
                            max=pmax,
                            min=pmin))
                            )]

            elif(protocoll=="1"):
                if(pmax==None):
                    ingress_security_rules=[oci.core.models.IngressSecurityRule(
                    description=desc,protocol=protocoll,
                    source=sourcee,
                    is_stateless=False,
                    source_type="CIDR_BLOCK",
                    icmp_options=None)]
                else:
                    ingress_security_rules=[oci.core.models.IngressSecurityRule(
                    description=desc,protocol=protocoll,
                    source=sourcee,
                    is_stateless=False,
                    source_type="CIDR_BLOCK",
                    icmp_options=oci.core.models.IcmpOptions(
                        code=pmin,
                        type=pmax)
                            )]
            elif(protocoll=="58"):
                if(pmax==None):
                    ingress_security_rules=[oci.core.models.IngressSecurityRule(
                    description=desc,protocol=protocoll,
                    source=sourcee,
                    is_stateless=False,
                    source_type="CIDR_BLOCK",
                    tcp_options=None)]
                else:
                    ingress_security_rules=[oci.core.models.IngressSecurityRule(
                    description=desc,protocol=protocoll,
                    source=sourcee,
                    is_stateless=False,
                    source_type="CIDR_BLOCK",
                    icmp_options=oci.core.models.IcmpOptions(
                        code=pmin,
                        type=pmax)
                            )]
            elif(protocoll=="all"):
                ingress_security_rules=[oci.core.models.IngressSecurityRule(
                    description=desc,protocol=protocoll,
                    source=sourcee,
                    is_stateless=False,
                    source_type="CIDR_BLOCK"
                    
                        )
                            ]

            # Check for matching values in security list
            for x in ingress_security_rules:
                for y in new_ingress_security_rules:
                    if(x ==y):
                        new_ingress_security_rules.remove(x)
            # Update the security list with the edited security rules 
                     
            update_security_list_details=oci.core.models.UpdateSecurityListDetails(
                display_name=current_security_list.display_name,
                ingress_security_rules=new_ingress_security_rules)

            update_security_list_response = core_client.update_security_list(
                security_list_id=current_security_list.id,
                update_security_list_details=update_security_list_details)
            response=update_security_list_response.data
        except Exception as e:
            frappe.errprint(e.with_traceback())
            
            return {"error": True, "msg":e.with_traceback() }




#function to delete outbound rules
@frappe.whitelist(allow_guest=True)
def delete_egress_rule(descriptionn,protocoll,port_minn,port_maxx,destinationn):
        config = {
            "user": "ocid1.user.oc1..aaaaaaaaaiij2osjymqtlzx4s3fgxccf55leybpule5blsa6nqayscqpnqhq",
            "key_file": "/opt/bench/frappe-bench/apps/cloud/cloud/www/oci_api_key.pem",
            "fingerprint": "be:fd:ac:fd:e5:9f:68:e0:bd:83:dc:ab:a8:a0:38:81",
            "tenancy": "ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq",
            "region": "me-jeddah-1",
        }
        
        try:
            #  Initialize service client with config file
            core_client = oci.core.VirtualNetworkClient(config)
            identity_client = oci.identity.IdentityClient(config)
            # Provide details of security list 
            compartment_id="ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq"
            vcn_id="ocid1.vcn.oc1.me-jeddah-1.amaaaaaa62vcruya5myc3mreogctutotajwahpjepv3bim3dazwxac2jtrya"
            subnet_id="ocid1.subnet.oc1.me-jeddah-1.aaaaaaaawmnhlihg6euaspjqvkkhgb24tirpi5dhkhme47rk6c77fhfxl4ha"
            seclist_name="Default Security List for Hiba-test-subnet"
            name = sys.argv[0]
            desc=descriptionn
            pmax=port_maxx
            if(desc==""):
                desc=" "
            if (desc=='None'):
                desc=None
            else:
                desc=descriptionn
            if(port_maxx=='None'):
                pmax=None
            elif((port_maxx==" ")|(port_maxx=="")): 
                pmax=None
                pmin=None
                



            else:
                pmax=int(port_maxx)
            pmin=port_minn
            if(pmin=='None'):
                pmin=None
            elif((port_minn==" ")|(port_minn=="")):
                pmin=None
            else:
                pmin=int(port_minn)
            
            if len(sys.argv) >= 3:
                new_ip = sys.argv[2]
            else:
                new_ip = None
            # List the rules available in the security list
            list_security_lists_response = core_client.list_security_lists(
                compartment_id=compartment_id,
                display_name=seclist_name,
                sort_order="DESC")
            current_security_list = list_security_lists_response.data[0]
            # Add them to a list named new_ingress_security_list
            new_egress_security_rules = []
            found_name = False
            if len(current_security_list.egress_security_rules) > 0:
                for il in current_security_list.egress_security_rules:
                    if il.description == name:
                        found_name = True
                        
                        if new_ip != None:
                            il.source = new_ip+'/32'
                            new_egress_security_rules.append(il)
                    else:
                        new_egress_security_rules.append(il)
            # Provide details of security rule to be deleted
            if(protocoll=='6'):
                if(pmax==None):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=protocoll,
                    destination=destinationn,
                    is_stateless=False,
                    destination_type="CIDR_BLOCK",
                    tcp_options=None)]
                else:
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=protocoll,
                    destination=destinationn,
                    is_stateless=False,
                    destination_type="CIDR_BLOCK",
                    tcp_options=oci.core.models.TcpOptions(
                        destination_port_range=oci.core.models.PortRange(
                            max=pmax,
                            min=pmin))
                            )]
                
            elif(protocoll=="17"):
                if(pmax==None):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=protocoll,
                    destination=destinationn,
                    is_stateless=False,
                    destination_type="CIDR_BLOCK",
                    udp_options=None)]
                else:
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=protocoll,
                    destination=destinationn,
                    is_stateless=False,
                    destination_type="CIDR_BLOCK",
                    udp_options=oci.core.models.UdpOptions(
                        destination_port_range=oci.core.models.PortRange(
                            max=pmax,
                            min=pmin))
                            )]

            elif(protocoll=="1"):
                if((pmax==None)&(pmin==None)):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=protocoll,
                    destination=destinationn,
                    is_stateless=False,
                    destination_type="CIDR_BLOCK",
                    icmp_options=None)]
                elif(pmax==None):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=protocoll,
                    destination=destinationn,
                    is_stateless=False,
                    destination_type="CIDR_BLOCK",
                    icmp_options=oci.core.models.IcmpOptions(
                        code=None,
                        type=pmin)
                            )]
                elif(pmin==None):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=protocoll,
                    destination=destinationn,
                    is_stateless=False,
                    destination_type="CIDR_BLOCK",
                    icmp_options=oci.core.models.IcmpOptions(
                        code=pmax,
                        type=None)
                            )]
                else:
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=protocoll,
                    destination=destinationn,
                    is_stateless=False,
                    destination_type="CIDR_BLOCK",
                    icmp_options=oci.core.models.IcmpOptions(
                        code=pmin,
                        type=pmax)
                            )]
            elif(protocoll=="58"):
                if((pmax==None)&(pmin==None)):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=protocoll,
                    destination=destinationn,
                    is_stateless=False,
                    destination_type="CIDR_BLOCK",
                    icmp_options=None)]
                elif(pmax==None):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=protocoll,
                    destination=destinationn,
                    is_stateless=False,
                    destination_type="CIDR_BLOCK",
                    icmp_options=oci.core.models.IcmpOptions(
                        code=None,
                        type=pmin)
                            )]
                elif(pmin==None):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=protocoll,
                    destination=destinationn,
                    is_stateless=False,
                    destination_type="CIDR_BLOCK",
                    icmp_options=oci.core.models.IcmpOptions(
                        code=pmax,
                        type=None)
                            )]
                else:
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=protocoll,
                    destination=destinationn,
                    is_stateless=False,
                    destination_type="CIDR_BLOCK",
                    icmp_options=oci.core.models.IcmpOptions(
                        code=pmax,
                        type=pmin)
                            )]
            elif(protocoll=="all"):
                egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=protocoll,
                    destination=destinationn,
                    is_stateless=False,
                    destination_type="CIDR_BLOCK"
                    
                        )
                            ]

            # Check for matching values in security list
            for x in egress_security_rules:
                for y in new_egress_security_rules:
                    if(x ==y):
                        new_egress_security_rules.remove(x)
            # Update the security list with the edited security rules 
                     
            update_security_list_details=oci.core.models.UpdateSecurityListDetails(
                display_name=current_security_list.display_name,
                egress_security_rules=new_egress_security_rules)

            update_security_list_response = core_client.update_security_list(
                security_list_id=current_security_list.id,
                update_security_list_details=update_security_list_details)
            response=update_security_list_response.data
        except Exception as e:
            frappe.errprint(e.with_traceback())
            
            return {"error": True, "msg":e.with_traceback() }


#function to get context
def get_context(context):
    datas = security_list_view()
    datax=egress_rules_list_view()
    
    context = {
        "datas": datas,
        "datax":datax        
    }
    return context