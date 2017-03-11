// moodbox.js

$(document).ready(function(){

  setInterval(requestUpdate, 1000);

});

function requestUpdate()
{
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
      $("#track_name").text(data[0].title);
      $("#album_artwork").attr("src",data[0].artwork);
      $("#track_artist").text(data[0].artist);
    }

  })
}
