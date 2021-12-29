const div =  document.querySelector('.my-4');
    div.classList.remove('container');
    div.classList.remove('my-4');
    // code for inserting question to doc
$(document).ready(function(){
        $('#button').click(function(){
          var title=$('#title').val();
          var body=$('#body').val();
          frappe.call({
            method: "quickfix.www.askquestion.insert_question",
            args:{
              title:title,body:body
            },
            callback: function(a) {
              
              frappe.msgprint({
                title: __('Notification'),
                indicator: 'green',
                message: __('Question added successfully')
      });
            }
          });

        })
    })