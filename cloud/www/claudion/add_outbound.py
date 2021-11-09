import frappe
import oci
from frappe.model.document import Document
import sys






@frappe.whitelist(allow_guest=True)     
def addd_egress_rule(desc,protocol,desti,p_max,p_min):  
            # Create a default configuration file 
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
            # Provide the details of security list to which rule is to be added
            compartment_id="ocid1.tenancy.oc1..aaaaaaaanvukpti3fx452gsvczw64d6dm2unoe6hgn6h5jkcainzmuej2tbq"
            vcn_id="ocid1.vcn.oc1.me-jeddah-1.amaaaaaa62vcruya5myc3mreogctutotajwahpjepv3bim3dazwxac2jtrya"
            subnet_id="ocid1.subnet.oc1.me-jeddah-1.aaaaaaaawmnhlihg6euaspjqvkkhgb24tirpi5dhkhme47rk6c77fhfxl4ha"
            seclist_name="Default Security List for Hiba-test-subnet"
            name = sys.argv[0]
            
            if(protocol=='TCP'):
                prot='6'
            if(protocol=="UDP"):
                prot='17'
            if(protocol=="ICMP"):
                prot='1'
            if(protocol=='ICMPV4'):
                prot='58'
            if(protocol=='All'):
                prot='all'
            if((p_max=="")|(p_max==" ")):
                pmax=None
            else:
                pmax=int(p_max)
            if((p_min=="")|(p_min==" ")):
                pmin=None
            else:
                pmin=int(p_min)
            if(desc==""):
                desc=" "
            # Request service for the details of current security list
            list_security_lists_response = core_client.list_security_lists(
                compartment_id=compartment_id,
                display_name=seclist_name,
                sort_order="DESC")
            current_security_list = list_security_lists_response.data[0]

            
            new_egress_security_rules = []

            if len(current_security_list.egress_security_rules) > 0:
                for il in current_security_list.egress_security_rules:
                    if il.description == name:
                        found_name = True
                        print(il.source)
                        if new_ip != None:
                            il.source = new_ip+'/32'
                            new_egress_security_rules.append(il)
                    else:
                        new_egress_security_rules.append(il)
            # Add new rule to the list
            if(prot=='6'):
                if(pmax==None):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=prot,
                    destination=desti,
                    tcp_options=None)]
                else:       
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=prot,
                    destination=desti,
                    tcp_options=oci.core.models.TcpOptions(
                        destination_port_range=oci.core.models.PortRange(
                            max=pmax,
                            min=pmin))
                            )
                           ]
            elif(prot=='17'):
                if(pmax==None):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=prot,
                    destination=desti,
                    udp_options=None)]
                else:
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,
                    protocol=prot,
                    destination=desti,
                    udp_options=oci.core.models.UdpOptions(
                    destination_port_range=oci.core.models.PortRange(
                            max=pmax,
                            min=pmin)))]
            if(prot=='1'):
                if((pmax==None)&(pmin==None)):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=prot,
                    destination=desti,
                    icmp_options=None)]
                elif(pmax==None):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,
                    protocol=prot,
                    destination=desti,
                    icmp_options=oci.core.models.IcmpOptions(
                        code=pmin,
                        type=None)
                    
                            )]
                elif(pmin==None):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,
                    protocol=prot,
                    destination=desti,
                    icmp_options=oci.core.models.IcmpOptions(
                        code=None,
                        type=pmax)
                    
                            )]

                else:
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,
                    protocol=prot,
                    destination=desti,
                    icmp_options=oci.core.models.IcmpOptions(
                        code=pmin,
                        type=pmax)
                    
                            )]
            if(prot=='58'):
                if((pmax==None)&(pmin==None)):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,protocol=prot,
                    destination=desti,
                    icmp_options=None)]
                elif(pmax==None):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,
                    protocol=prot,
                    destination=desti,
                    icmp_options=oci.core.models.IcmpOptions(
                        code=pmin,
                        type=None)
                    
                            )]
                elif(pmin==None):
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,
                    protocol=prot,
                    destination=desti,
                    icmp_options=oci.core.models.IcmpOptions(
                        code=None,
                        type=pmax)
                    
                            )]

                else:
                    egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,
                    protocol=prot,
                    destination=desti,
                    icmp_options=oci.core.models.IcmpOptions(
                        code=pmax,
                        type=pmin)
                    
                            )]
            if(prot=="all"):
                egress_security_rules=[oci.core.models.EgressSecurityRule(
                    description=desc,
                    protocol=prot,
                    destination=desti)]
                
            new_egress_security_rules.extend(egress_security_rules)
            # Update the security list with the new rule
            update_security_list_details=oci.core.models.UpdateSecurityListDetails(
                display_name=current_security_list.display_name,
                egress_security_rules=new_egress_security_rules)

            update_security_list_response = core_client.update_security_list(
                security_list_id=current_security_list.id,
                update_security_list_details=update_security_list_details)
            respon=update_security_list_response.data
            json2={"response":respon.id}
        except Exception as e:
            frappe.errprint(e.with_traceback())
            
            return {"error": True, "msg":e.with_traceback() }   
