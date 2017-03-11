// moodbox.js

$(document).ready(function(){

  setTimeout(function(){
    // http://localhost/api.php?action=update
    var jqxhr = $.getJSON('http://drop.robbie.xyz/fbmoodbox/dummyjson.json',function(data){
      // console.log("success");

      //var data = JSON.parse(e.responseText);

      console.log(data);

      // If data is an empty object
      if(data.length == 0)
      {

      }
      else
      {
        $("#track_name").text(data[0].title)
      }

    })
    .fail(function(e){
      //console.log(e.responseText);


    })

  }, 1000);

});
