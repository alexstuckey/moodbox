// moodbox.js

$(document).ready(function(){

  setTimeout(function(){
    // http://localhost/api.php?action=update
    var jqxhr = $.getJSON('http://drop.robbie.xyz/fbmoodbox/dummyjson.json',function(data){
      console.log(data);
    })
    .fail(function(e){
      console.log(e.responseText);
      console.log(JSON.parse(e.responseText));
    })

  }, 1000);

});
