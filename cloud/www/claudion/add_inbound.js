const div = document.querySelector('.my-4');
div.classList.remove('container');
div.classList.remove('my-4');
// Deals with viewingg fields in form
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
        $('#otherFieldDiv1').hide();
        $('#otherFieldDiv').hide();
    }
});
// Gets the value from form fields
$(document).ready(function () {
    $('#button').click(function () {
        var source = $('#source').val();
        var protocol = $('#seeAnotherField').find(":selected").text();
        var dport = $('#d-port').val();
        var sport = $('#s-port').val();
        var description = $('#description').val();
        var type = $('#type').val();
        var code = $('#code').val();
        console.log(typeof (description))
        // Calling function to add rule 
        if (protocol == "TCP" || protocol == "UDP") {
            frappe.call({
                method: "cloud.www.claudion.add_inbound.addd_ingress_rule",
                args: {
                    protocol: protocol, sour: source, desc: description, p_max: dport, p_min: dport
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
                method: "cloud.www.claudion.add_inbound.addd_ingress_rule",
                args: {
                    protocol: protocol, sour: source, desc: description, p_max: type, p_min: code
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
                method: "cloud.www.claudion.add_inbound.addd_ingress_rule",
                args: {
                    protocol: protocol, sour: source, desc: description, p_max: "", p_min: ""
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