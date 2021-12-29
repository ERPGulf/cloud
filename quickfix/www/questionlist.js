const div =  document.querySelector('.my-4');
    div.classList.remove('container');
    div.classList.remove('my-4');
    
// code searching question in database and displaying them
function search_question() {
    let input = document.getElementById('searchbar').value
    
    input=input.toLowerCase();
    
   
    frappe.call({
        method: "quickfix.www.questionlist.search_question",
        args:{
          keyword : input
        },
        callback: function(a) {
          x=a.message
          
         title=[]
         body=[]
         
    for (i=0;i<x.length;i++){
      
      let dataa=a.message[i][0]
      title.push(dataa)
      let dataaa=a.message[i][1]
      body.push(dataaa)

    }
    ul = document.createElement('ul');

    document.getElementById('searchList').appendChild(ul);
    
    title.forEach(function (item) {
        let li = document.createElement('li');
        ul.appendChild(li);
    
        li.innerHTML += item;
    }); 
    
    }
    });

    let x = document.getElementsByClassName('question');
    console.log(x)
    for (i = 0; i < x.length; i++) { 
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="list-item";                 
        }
    }
  }

  $(document).ready(function(){
    $('#search_qn').click(function(){
      var keyword=$('#searchbar').val();
      console.log(keyword)
      frappe.call({
        method: "quickfix.www.questionlist.search_question",
        args:{
          keyword : keyword
        },
        callback: function(a) {
          x=a.message
          console.log(x)
         title=[]
         body=[]
         
    for (i=0;i<x.length;i++){
      
      let dataa=a.message[i][0]
      title.push(dataa)
      let dataaa=a.message[i][1]
      body.push(dataaa)
      var loc = "/answer.html?title="+dataa[i];
          

    }
    $('.question').hide();
    ol = document.createElement('ol');

    document.getElementById('searchList').appendChild(ol);
    
    title.forEach(function (item) {
        var li = document.createElement('li');
        
      
        ol.appendChild(li);
       
        li.innerHTML += item.link("/answer.html?title="+item)
        
    });
          
 
        }
      });

    })
})