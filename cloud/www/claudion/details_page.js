
// to remove the extra container and space in page
const div = document.querySelector('.my-4');
div.classList.remove('container');
div.classList.remove('my-4');




// function to fetch the status of the instance
function set_status() {
    text = document.getElementById('oci_id').textContent
    comp_id = document.getElementById('compartment_id').textContent
    
    frappe.call({
        method: "cloud.utils.intnc_stat",
        args: {
            current_oci_id: text,
            compartment_id:comp_id

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
    comp_id = document.getElementById('compartment_id').textContent

    frappe.call({
        method: "cloud.utils.get_public_ip",
        args: {
            current_oci_id: text,
            compartment_id:comp_id

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
    comp_id = document.getElementById('compartment_id').textContent

    frappe.call({
        method: "cloud.utils.get_private_ip",
        args: {
            current_oci_id: text,
            compartment_id:comp_id

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
    graph();
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

// Call the function
function graph() {
    frappe.call({
        method: "cloud.utils.metrics_graph",

        callback: function (a) {
            // Collect data returned by function 
            var data = a.message.data
            var data1 = a.message.data1
            var time = a.message.time
            var data2 = a.message.data2
            var data3 = a.message.data3
            var data4 = a.message.data4
            var data5 = a.message.data5
            var data6 = a.message.data6
            var data7 = a.message.data7
            var data8 = a.message.data8
            var data9 = a.message.data9
            console.log(data8)
            // Plot graphs using the data recieved
            var trace1 = {
                x: time,
                y: data,
                type: 'scatter'
            };

            var trace2 = {
                x: time,
                y: data1,
                xaxis: 'x2',
                yaxis: 'y2',
                type: 'scatter'
            };

            var trace3 = {
                x: time,
                y: data2,
                xaxis: 'x3',
                yaxis: 'y3',
                type: 'scatter'
            };

            var trace4 = {
                x: time,
                y: data3,
                xaxis: 'x4',
                yaxis: 'y4',
                type: 'scatter'
            };
            var trace5 = {
                x: time,
                y: data4,
                xaxis: 'x5',
                yaxis: 'y5',
                type: 'scatter'
            };
            var trace6 = {
                x: time,
                y: data5,
                xaxis: 'x6',
                yaxis: 'y6',
                type: 'scatter'
            };
            var trace7 = {
                x: time,
                y: data6,
                xaxis: 'x7',
                yaxis: 'y7',
                type: 'scatter'
            };
            var trace8 = {
                x: time,
                y: data7,
                xaxis: 'x8',
                yaxis: 'y8',
                type: 'scatter'
            };
            var trace9 = {
                x: time,
                y: data8,
                xaxis: 'x9',
                yaxis: 'y9',
                type: 'scatter'
            };
            var trace10 = {
                x: time,
                y: data9,
                xaxis: 'x10',
                yaxis: 'y10',
                type: 'scatter'
            };
            var data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10];
            // Specify layout of graphs
            var layout = {
                grid: { rows: 6, columns: 2, pattern: 'independent' },
                width: 1000,
                height: 1500,
                showlegend: false,
                annotations: [{
                    text: "Memory Utilization",
                    font: {
                        size: 13,
                        color: '#32363b',
                    },
                    showarrow: false,
                    align: 'center',
                    x: 0.13, //position in x domain
                    y: 1.02, //position in y domain
                    xref: 'paper',
                    yref: 'paper',
                }, {
                    text: "CPU Utilization",
                    font: {
                        size: 13,
                        color: '#32363b',
                    },
                    showarrow: false,
                    align: 'center',
                    x: 0.85, //position in x domain
                    y: 1.02, //position in y domain
                    xref: 'paper',
                    yref: 'paper',
                }, {
                    text: "Disk IO  Read",
                    font: {
                        size: 13,
                        color: '#32363b',
                    },
                    showarrow: false,
                    align: 'center',
                    x: 0.13, //position in x domain
                    y: 0.832, //position in y domain
                    xref: 'paper',
                    yref: 'paper',
                }, {
                    text: "Disk IO Write",
                    font: {
                        size: 13,
                        color: '#32363b',
                    },
                    showarrow: false,
                    align: 'center',
                    x: 0.85, //position in x domain
                    y: 0.832, //position in y domain
                    xref: 'paper',
                    yref: 'paper',
                }, {
                    text: "Disk Write Bytes",
                    font: {
                        size: 13,
                        color: '#32363b',
                    },
                    showarrow: false,
                    align: 'center',
                    x: 0.13, //position in x domain
                    y: 0.67, //position in y domain
                    xref: 'paper',
                    yref: 'paper',
                }, {
                    text: "Disk Read Bytes",
                    font: {
                        size: 13,
                        color: '#32363b',
                    },
                    showarrow: false,
                    align: 'center',
                    x: 0.85, //position in x domain
                    y: 0.67, //position in y domain
                    xref: 'paper',
                    yref: 'paper',
                }, {
                    text: "Network Receive Bytes",
                    font: {
                        size: 13,
                        color: '#32363b',
                    },
                    showarrow: false,
                    align: 'center',
                    x: 0.13, //position in x domain
                    y: 0.487, //position in y domain
                    xref: 'paper',
                    yref: 'paper',
                }, {
                    text: "Network Transmit Bytes",
                    font: {
                        size: 13,
                        color: '#32363b',
                    },
                    showarrow: false,
                    align: 'center',
                    x: 0.899, //position in x domain
                    y: 0.487, //position in y domain
                    xref: 'paper',
                    yref: 'paper',
                }, {
                    text: "Load Average",
                    font: {
                        size: 13,
                        color: '#32363b',
                    },
                    showarrow: false,
                    align: 'center',
                    x: 0.13, //position in x domain
                    y: 0.29999, //position in y domain
                    xref: 'paper',
                    yref: 'paper',
                }, {
                    text: "Memory Allocation Stalls",
                    font: {
                        size: 13,
                        color: '#32363b',
                    },
                    showarrow: false,
                    align: 'center',
                    x: 0.899, //position in x domain
                    y: 0.2999, //position in y domain
                    xref: 'paper',
                    yref: 'paper',
                }]
            };
            var config = {
                displayModeBar: false
            }
            // plot graph using data
            Plotly.newPlot('myDiv', data, layout, config);
        }

    })

}
