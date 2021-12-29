const div =  document.querySelector('.my-4');
    div.classList.remove('container');
    div.classList.remove('my-4');
// code for getting title of page
var getUrlParameter = function getUrlParameter(sParam) {
  var sPageURL = window.location.search.substring(1),
      sURLVariables = sPageURL.split('&'),
      sParameterName,
      i;

  for (i = 0; i < sURLVariables.length; i++) {
      sParameterName = sURLVariables[i].split('=');

      if (sParameterName[0] === sParam) {
          return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
      }
  }
  return false;
};
var titlee=getUrlParameter("title")

// load question title and question body from doctype and adding them to html list

$(document).ready( function () {
  document.getElementById("question_title").innerHTML = titlee;
  frappe.call({
    method: "quickfix.www.answer.get_questionbody",
    args:{title:titlee},
  
    callback: function(a) {
  b=a.message[0][0]
  console.log(b)
      document.getElementById("question_body").innerHTML = b;
      
    }
  });
frappe.call({
  method: "quickfix.www.answer.get_answers",
  args:{title:titlee},

  callback: function(a) {

    var x=a.message
    items=[]
    for (i=0;i<x.length;i++){
      let dataa=a.message[i].answer
      items.push(dataa)

    }
    ul = document.createElement('ul');

    document.getElementById('myList').appendChild(ul);
    
    items.forEach(function (item) {
        let li = document.createElement('li');
        ul.appendChild(li);
    
        li.innerHTML += item;
    }); 
    
  }
});

})
// code for adding answer to doctype
function showInput() {
  var ans= document.getElementById("user_input").value;
 frappe.call({
     method: "quickfix.www.answer.insert_answer",
     args:{answer:ans,title:titlee},
     callback: function(a) {
       
       frappe.msgprint({
         title: __('Notification'),
         indicator: 'green',
         message: __('Answer added successfully')
});
location.reload()
     }
   });

}