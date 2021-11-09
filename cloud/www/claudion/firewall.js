const div = document.querySelector('.my-4');
div.classList.remove('container');
div.classList.remove('my-4');


$(document).ready(function () {
    let deleteelement;
    // Code to read selected table row cell data (values).
    $("#mytable").on('click', '.btn-sm', function () {
        // Get the current row
        var currentRow = $(this).closest("tr");
        deleteelement = $(this).closest("tr")
        // Gets the data from form fields
        var source = currentRow.find("td:eq(0)").html();
        var protocol = currentRow.find("td:eq(1)").html();
        var port_max = currentRow.find("td:eq(2)").html();
        var port_min = currentRow.find("td:eq(3)").html();
        var description = currentRow.find("td:eq(4)").html();
        // Call to the functions to delete rule
        frappe.call({
            method: "cloud.www.claudion.firewall.delete_ingress_rule",
            args: {
                descriptionn: description, protocoll: protocol, sourcee: source, port_maxx: port_max, port_minn: port_min
            },
            callback: function (a) {
                deleteelement.remove();
                frappe.msgprint({
                    title: __('Notification'),
                    indicator: 'green',
                    message: __('Firewall rule deleted successfully')
                });
            }
        });

    })
    $("#mytable1").on('click', '.btn-sm', function () {
        // Get the current row
        var currentRow = $(this).closest("tr");
        deleteelement = $(this).closest("tr")
        // Gets the data from form fields
        var destination = currentRow.find("td:eq(0)").html();
        var protocol = currentRow.find("td:eq(1)").html();
        var port_max = currentRow.find("td:eq(2)").html();
        var port_min = currentRow.find("td:eq(3)").html();
        var description = currentRow.find("td:eq(4)").html();
        // Call to the functions to delete rule
        frappe.call({
            method: "cloud.www.claudion.firewall.delete_egress_rule",
            args: {
                descriptionn: description, protocoll: protocol, destinationn: destination, port_maxx: port_max, port_minn: port_min // taking the oci id as argument for the function
            },
            callback: function (a) {
                deleteelement.remove();
                frappe.msgprint({
                    title: __('Notification'),
                    indicator: 'green',
                    message: __('Firewall rule deleted successfully')
                });
            }
        });

    })

});