// Copyright (c) 2021, cloud and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cloud', {
	before_load: function(frm) {       // function to get the ip address and status of the instance before the document is load after it inserted to the database
		
		if(frm.doc.oci){

			frappe.call({
				method:"cloud.cloud.doctype.cloud.cloud.get_public_id", //to get the public_ip of the current instance
				args:{
				current_oci_id:frm.doc.oci    // taking the oci id as argument for the function
				}, 
				callback:function(r){
					frm.set_value("public_ip",String(Object.values(r))) // setting the public ip to the feild and converting it to string
					
				},
			}); 
			frappe.call({
				method:"cloud.cloud.doctype.cloud.cloud.get_private_id",   //to get the private_ip of the current instance
				args:{
				current_oci_id:frm.doc.oci
				}, 
				callback:function(r){
					frm.set_value("private_ip",String(Object.values(r))) // setting the public ip to the feild and converting it to string
					 
				},
			});
			frappe.call({
				method:"cloud.cloud.doctype.cloud.cloud.intnc_stat",  //to get the public_id of the current instance
				args:{
				status_oci:frm.doc.oci
				}, 
				callback:function(r){
					frm.set_value("stat",String(Object.values(r))) // setting the public ip to the feild and converting it to string
					 
				},
			});
			
		}
	},
	onload_post_render:function(frm){   //function to save the document automatically after the instance is created and the status and ip are fetched
		if(frm.doc.status="RUNNING" && frm.doc.oci){
			frm.save();
		}
		
	},
});
