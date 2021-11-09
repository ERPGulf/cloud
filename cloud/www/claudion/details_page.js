
// to remove the extra container and space in page
const div = document.querySelector('.my-4');
div.classList.remove('container');
div.classList.remove('my-4');

// function to fetch the status of the instance
function set_status() {
	text = document.getElementById('oci_id').textContent
	frappe.call({
		method: "cloud.utils.intnc_stat",
		args: {
			current_oci_id: text
		},
		callback: function (a) {
			var s = document.getElementById('status');
			data = String(Object.values(a))
			s.innerHTML = data
			if (data == "RUNNING") {
				document.getElementById('status').style.color = 'green'
				$(".poweron").hide();
			}
			else if (data == "STOPPED") {
				document.getElementById('status').style.color = 'red'
				$(".poweroff").hide();
			}
			else if (data == "STOPPING") {
				document.getElementById('status').style.color = 'red'
				$(".poweroff").hide();
				$(".poweron").hide();
				$(".reboot").hide();
			}
			else if (data == "STARTING") {
				document.getElementById('status').style.color = 'green'
				$(".poweroff").hide();
				$(".poweron").hide();
				$(".reboot").hide();
			}
			else {
				$(".poweroff").hide();
				$(".poweron").hide();
				$(".reboot").hide();

			}
		}
	});
}


//function to fetch the public_ip of the instance
function set_public_ip() {
	text = document.getElementById('oci_id').textContent
	frappe.call({
		method: "cloud.utils.get_public_ip",
		args: {
			current_oci_id: text
		},
		callback: function (a) {
			var s = document.getElementById('public_ip');
			data = String(Object.values(a))
			s.innerHTML = data
		}
	});
}


//function to fetch the private_ip of the instance
function set_private_ip() {
	text = document.getElementById('oci_id').textContent
	frappe.call({
		method: "cloud.utils.get_private_ip",
		args: {
			current_oci_id: text
		},
		callback: function (a) {
			var s = document.getElementById('private_ip');
			data = String(Object.values(a))
			s.innerHTML = data

		}
	});
}
//declaring the functions when page reload
window.onload = function () {

	set_status();
	set_public_ip();
	set_private_ip();
}

// function to poweroff the instance
function ins_poweroff() {
	text = document.getElementById('oci_id').textContent
	console.log(text);
	frappe.call({
		method: "cloud.utils.instance_poweroff",
		args: {
			current_oci_id: text
		},
		callback: function (a) {
			console.log(a);
		}
	});
}


// function to poweron the instance
function ins_poweron() {
	text = document.getElementById('oci_id').textContent
	console.log(text);
	frappe.call({
		method: "cloud.utils.instance_poweron",
		args: {
			current_oci_id: text
		},
		callback: function (a) {
			console.log(a);
			
		}
	});
}

// function to reboot the instance
function ins_reboot() {
	text = document.getElementById('oci_id').textContent
	console.log(text);
	frappe.call({
		method: "cloud.utils.instance_reboot",
		args: {
			current_oci_id: text
		},
		callback: function (a) {
			console.log(a);
			
		}
	});
}

// function to display the confomation toast 
var CustomConfirm = new function () {
	this.show = function (msg, callback) {
		var dlg = document.getElementById('dialogCont')
		var dlgBody = dlg.querySelector('#dlgBody')
		dlg.style.top = "40%"
		dlg.style.opacity = 1;
		dlgBody.textContent = msg;
		this.callback = callback
		document.getElementById("freezeLayer").style.display = ''
	};
	this.okey = function () {
		this.callback();
		window.location = ""
		this.close();
	}
	this.close = function () {
		var dlg = document.getElementById('dialogCont')
		dlg.style.top = "-40%"
		dlg.style.opacity = 0;
		document.getElementById("freezeLayer").style.display = 'none'

	}
}

function ins_delete() {
	window.location = ""
}