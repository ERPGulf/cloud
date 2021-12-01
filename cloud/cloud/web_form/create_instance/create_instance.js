


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
	<h3>Cloud Server Details</h3>
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

	<link rel="stylesheet" href="/assets/cloud/css/main_style.css">


<div class="sidenav">
    <!-- Sidebar start -->
    <nav id="sidebar" class="sidebar-main">


        <ul class="list-unstyled components">

            <li>
                <a href="/claudion/index">Cloud Server</a>
            </li>
            <li>
                <a href="/claudion/firewall">Firewalls</a>
            </li>

        </ul>
    </nav>
</div>
    
    <div class="table-sec">
        <div class="main" id="content">
    
    </div></div>`);

	
	// moving the the form-label-part div inside the side bar div of id content
	var fragment = document.createDocumentFragment();
	fragment.appendChild(document.querySelector('.form-label-part'));
	document.querySelector('#content').appendChild(fragment);


	
	
	
	
	// to get the username 
	frappe.web_form.after_load = () => {
		frappe.web_form.set_value('email',frappe.session.user);
		// function call to fetch username from db
		frappe.call({
			method: "cloud.utils.get_username",
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
					method: "cloud.utils.get_billing_intervell",
					args: {
						value: value ,
					},
					callback: function(plan){
						frappe.web_form.set_value('billing_intervell', String(Object.values(plan)));
						
					},
				});

				// function to get the price per month in webform after selecting the paln
				frappe.call({

					method: "cloud.utils.price_per_month",
					args: {
						value: value ,
					},
					callback: function(plan){
						data=document.querySelector('.cost').innerHTML=`<p class="month-cost">${String(Object.values(plan))}$/mo</p>`
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
		//seting distributions section in the form of cards
		var regiondiv = document.querySelector('.form-section:nth-child(1)');
		regiondiv.innerHTML=`
		
		<div>
		<h5 class="region-heading">Choose a distribution</h5>
		<div class="row" >
		{%for distribution in distributions%}
			
		<div class="card distri-card" onclick='distri_onclick_function("{{distribution.distributions_name}}")'>
  			<img class="card-img-top distri-img" src="{{distribution.image}}" alt="Card image cap">
  			<div class="card-body">
    		<p class="distri-card-text" id="get-distri-{{distribution.distributions_name}}">{{distribution.distributions_name}}</p>
  			</div>
		</div>
		  {%endfor%}
		  </div>
		  </div>
		`


		//seting region section in the form of cards
		var regiondiv = document.querySelector('.form-section:nth-child(2)');
		regiondiv.innerHTML=`
		
		<div>
		<h5 class="region-heading">Choose a datacenter region</h5>
		<div class="row" >
		{%for region in regions%}
			<div  class="card region-card" onclick='region_onclick_function("{{region.region}}")'>
        	<div class="card-body">
            <img src="{{region.image}}" class="flag-icon" id="dta">
          	<p class="reg-card-head" id="get-region-{{region.region}}">{{region.region}}</p>
        	</div>
      		</div> 
		  {%endfor%}
		  </div>
		  </div>
		`


		//seting plan section in the form of cards
		var plandiv=document.querySelector('.form-section:nth-child(3)')
		plandiv.innerHTML=`
		<div>
			<h5 class="region-heading">Choose a plan</h5>
			<div class="row" >
			{%for plan in plans%}
			<div onclick='plan_onclick_function("{{plan.plan_name}}")' class="card plan-card"  style="max-width: 18rem;">
			<div class="card-header plan-card-head">$ {{plan.cost}}/mo</div>
			<div class="card-body">
			<p class="card-title" id="get-plan-{{plan.plan_name}}">{{plan.plan_name}}</p>
			<p class="card-text">Item: {{plan.item}}</p>
			</div>
		</div>
			{%endfor%}
			</div>
			</div>
		`
	}

	// function to navigate the webform after the submiting the form
	frappe.web_form.after_save = () => {
		window.location.href = "/claudion/index";
	  }
	
})
//onclick function to get the region by clicking the region card
function region_onclick_function(region){
	var set=document.getElementById('get-region-'+region).innerText
	frappe.web_form.set_value('region', set);
	console.log(set);
}

//onclick function to get the plan by clicking the plan card
function plan_onclick_function(plan){
	var set=document.getElementById('get-plan-'+plan).innerText
	frappe.web_form.set_value('plan', set);
	console.log(set);
}
//onclick function to get the distribution by clicking the distribution card
function distri_onclick_function(distri){
	var set=document.getElementById('get-distri-'+distri).innerText
	frappe.web_form.set_value('distributions', set);
	console.log(set);
}

//to make the region card active by clicking and make it deactive when clicking the other region card	
$(document).on('click','.region-card',function(){
    $(this).addClass('active').siblings().removeClass('active')
})
//to make the plan card active by clicking and make it deactive when clicking the other plan card	
$(document).on('click','.plan-card',function(){
    $(this).addClass('active').siblings().removeClass('active')
})

//to make the region card active by clicking and make it deactive when clicking the other region card	
$(document).on('click','.distri-card',function(){
    $(this).addClass('active').siblings().removeClass('active')
})




// function to delay the execution of the vcn creation call
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


// calling function when the create instance webform page loads
window.onload = function () {
	//frappe call to check is any compartment is created by the user
    frappe.call({
        method: "cloud.utils.get_name",
        args: {
            user_id: frappe.session.user
        },
        callback: function (b) {
            cmp_name = String(Object.values(b))
            if (cmp_name == 0) {
                //frappe call to create a compartment if no compartment is created by the user
                frappe.call({
                    method: "cloud.utils.create_compartment",
                    args: {
                        user_name: "test-deepak012",
                    },
                    callback: function (a) {
                        s = Object.values(a)
                        cmp_id = s[0]
                        sleep(6000).then(() => { //to set 6 second delay after creating a compartment
                            //frappe call to create vcn using the compartment id
                            frappe.call({
                                method: "cloud.utils.create_vcn",
                                args: {
                                    current_cmp_id: cmp_id
                                },
                                callback: function (b) {
                                    //frappe call to create a document to store the vcn_id and compartment_id in comp_id doctype
                                    frappe.call({
                                        method: "cloud.utils.save_cmp",
                                        args: {
                                            ai: String(Object.values(a)),
                                            bi: String(Object.values(b)),
                                            user: frappe.session.user,
                                        },
                                        callback: function (c) {
                                        }

                                    })
                                }
                            })
                        })


                    }
                })
            }
        }
    })

}

