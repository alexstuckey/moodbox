// moodbox.js

$(document).ready(function(){

  setTimeout(function(){
    // http://localhost/api.php?action=update
      $.getJSON('dummyjson.html',function(data){
          console.log(data);
      }
    );
  }, 1000);

});
