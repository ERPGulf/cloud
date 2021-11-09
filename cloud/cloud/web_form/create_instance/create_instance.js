


frappe.ready(function() {
	// removing the two class from the  main to get the full page
	const div =  document.querySelector('.my-4');
	div.classList.remove('container');
	div.classList.remove('my-4');
	
	// creating a new div with class name form-label-part inside the main tag
	var studentDiv = document.querySelector('div.page_content');
	studentDiv.insertAdjacentHTML('afterend','<div class="row form-label-part"></div>');

	
	// moving the page_content div inside the newly created form-label-part div
	var fragment = document.createDocumentFragment();
	fragment.appendChild(document.querySelector('.page_content'));
	document.querySelector('.form-label-part').appendChild(fragment);


	//giving the row class to the page_content div for dived to cloums
	document.querySelector('.page_content').className += ' col-xs-9'


	//creating another div of class summery for the instance summery
	var studentDiv = document.querySelector('div.page_content');
	studentDiv.insertAdjacentHTML('afterend',`<div class="summery col-xs-3">
	<h3>Instance Details</h3>
	<p class="label"></p>
	
	<p class="plan"></p>
	<p class="cost"></p>
	<a class="navigat-btn"></a>
	
	</div>`);

	
	// moving the create button to the summery div
	var fragment = document.createDocumentFragment();
	fragment.appendChild(document.querySelector('.web-form-footer'));
	document.querySelector('.navigat-btn').appendChild(fragment);



	//creating a div for the sidebar inside main
	var studentDiv = document.querySelector('.form-label-part');
	studentDiv.insertAdjacentHTML('afterend',`

	<link rel="stylesheet" href="/assets/cloud/css/style.css">

	<div class="wrapper">    
	<!-- Sidebar start -->
    <nav id="sidebar" class="sidebar-main">

        <ul class="list-unstyled components">
            
            <li>
                <a href="/index">Instance</a>
            </li>
            <li>
                <a href="/claudion/firewall">Firewall</a>
            </li>
            
            <li>
                <a href="#">Portfolio</a>
            </li>
            <li>
                <a href="#">Contact</a>
            </li>
        </ul>

        
    </nav>
    <div id="content" >
    
    </div></div>`);

	
	// moving the the form-label-part div inside the side bar div of id content
	var fragment = document.createDocumentFragment();
	fragment.appendChild(document.querySelector('.form-label-part'));
	document.querySelector('#content').appendChild(fragment);


	
	
	
	
	// to get the username and host name when we load the form
	frappe.web_form.after_load = () => {

		// function call to fetch username from db
		frappe.call({
			method: "linode.utils.get_username",
			args: {                               
				uid: frappe.session.user
			},
			callback: function(r){
				frappe.web_form.set_value('username', String(Object.values(r)));
			}
		}),

		// function to set the billing intervell based on the plan that the user give
		frappe.web_form.on('plan', (field, value) => {
			// cheking there is plan in the plan feild
			if (value) {
				data=document.querySelector('.plan').innerHTML=`Plan <br><b class="label-disp">${value}</b>`
				frappe.web_form.set_value(data,value);
				// fuction call to get the billin_intervell based on the plan
				frappe.call({
					method: "linode.utils.get_billing_intervell",
					args: {
						value: value ,
					},
					callback: function(plan){
						frappe.web_form.set_value('billing_intervell', String(Object.values(plan)));
						
					},
				});

				// function to get the price per month in webform after selecting the paln
				frappe.call({

					method: "linode.utils.price_per_month",
					args: {
						value: value ,
					},
					callback: function(plan){
						data=document.querySelector('.cost').innerHTML=`<p class="month-cost">${String(Object.values(plan))} /mo</p>`
						frappe.web_form.set_value(data, String(Object.values(plan)));
						
					},
				});
				
			}
		});
		// function to show the lable when it type in the feild
		frappe.web_form.on('label', (field, value) => {
			if (value) {
				data=document.querySelector('.label').innerHTML=`Instance Label <br><b class="label-disp">${value}</b><hr class="hr">`
				frappe.web_form.set_value(data,value);
				

			}

		})
	}

	// function to navigate the webform after the submiting the form
	frappe.web_form.after_save = () => {
		window.location.href = "/index";
	  }
	
})

document.querySelector('.form-section:nth-child(3)').innerHTML='<p>test</p>'
