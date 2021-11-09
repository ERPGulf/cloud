const div = document.querySelector('.my-4');
div.classList.remove('container');
div.classList.remove('my-4');


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
