// moodbox.js

window.data = {};

$(document).ready(function(){

  requestUpdate();

  setInterval(function(){requestUpdate()}, 1000);
  console.log("doc ready");

});

function requestUpdate()
{
  // http://localhost/api.php?action=update
  console.log("requested update");
  var jqxhr = $.getJSON('http://drop.robbie.xyz/fbmoodbox/dummyjson.json',function(d){

    console.log(d);
    data = d;

    // If data is an empty object
    if(data.length == 0)
    {

    }
    else
    {
      $("#track_name").text(data.queue[0].title);
      $("#album_artwork").attr("src",data.queue[0].artwork);
      $("#track_artist").text(data.queue[0].artist);
    }

  }).fail(function(e){console.log("error (probably invalid JSON)");console.log(e)})
}

function requestNextSong()
{
  // http://localhost/api.php?action=nextsong
  var jqxhr = $.getJSON('http://localhost/api.php?action=nextsong');
  $("#track_name").text(data.queue[1].title);
  $("#album_artwork").attr("src",data.queue[1].artwork);
  $("#track_artist").text(data.queue[1].artist);
}
