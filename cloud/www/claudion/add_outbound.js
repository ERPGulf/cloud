const div = document.querySelector('.my-4');
div.classList.remove('container');
div.classList.remove('my-4');
// Deals with visible content in form
$("#seeAnotherField").change(function () {

    if ($(this).val() == "no") {
        $('#otherFieldDiv').hide();
        $('#otherField').attr('required', '');
        $('#otherField').attr('data-error', 'This field is required.');
        $('#otherFieldDiv1').show();
        $('#otherField').removeAttr('required');
        $('#otherField').removeAttr('data-error');
    } else if ($(this).val() == "yes") {
        $('#otherFieldDiv').show();
        $('#otherField').removeAttr('required');
        $('#otherField').removeAttr('data-error');
        $('#otherFieldDiv1').hide();
        $('#otherField').attr('required', '');
        $('#otherField').attr('data-error', 'This field is required.');
    }
    else {
        $('#otherFieldDiv').hide();
        $('#otherFieldDiv1').hide();
    }
});
// Fetches data from form
$(document).ready(function () {
    $('#button').click(function () {
        var destination = $('#destination').val();
        var protocol = $('#seeAnotherField').find(":selected").text();
        var dport = $('#d-port').val();
        var sport = $('#s-port').val();
        var description = $('#description').val();
        var type = $('#type').val();
        var code = $('#code').val();
        console.log(typeof (description))
        // Calls to the function to add rule
        if (protocol == "TCP" || protocol == "UDP") {
            frappe.call({
                method: "cloud.www.claudion.add_outbound.addd_egress_rule",
                args: {
                    protocol: protocol, desti: destination, desc: description, p_max: sport, p_min: sport
                },
                callback: function (a) {
                    frappe.msgprint({
                        title: __('Notification'),
                        indicator: 'green',
                        message: __('Firewall rule added successfully')
                    });
                }
            });
        }
        if (protocol == "ICMP" || protocol == "ICMPV4") {


            frappe.call({
                method: "cloud.www.claudion.add_outbound.addd_egress_rule",
                args: {
                    protocol: protocol, desti: destination, desc: description, p_max: type, p_min: code
                },
                callback: function (a) {

                    frappe.msgprint({
                        title: __('Notification'),
                        indicator: 'green',
                        message: __('Firewall rule added successfully')
                    });
                }


            });


        }
        if (protocol == "All") {
            frappe.call({
                method: "cloud.www.claudion.add_outbound.addd_egress_rule",
                args: {
                    protocol: protocol, desti: destination, desc: description, p_max: "", p_min: ""
                },
                callback: function (a) {

                    frappe.msgprint({
                        title: __('Notification'),
                        indicator: 'green',
                        message: __('Firewall rule added successfully')
                    });
                }
            });

        }
        window.location = "/claudion/firewall"
    })
})
