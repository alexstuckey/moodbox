// moodbox.js

window.data = {};
window.playing = true;

var queue = [];

$(document).ready(function(){

  requestUpdate();

  changeTrack(queue[0].title, queue[0].artwork, queue[0].length, queue[0].artist);

  setInterval(function(){requestUpdate()}, 1000);
  console.log("doc ready");

});

function requestUpdate()
{
  // http://localhost/api.php?action=update
  console.log("requested update");
  var jqxhr = $.getJSON('http://drop.robbie.xyz/fbmoodbox/dummyjson.php',function(d){

    console.log(d);
    data = d;

    queue = data.queue;

  }).fail(function(e){
    console.log("error (probably invalid JSON)",e)});
}

function requestNextSong()
{
  // http://localhost/api.php?action=nextsong
  var jqxhr = $.getJSON('http://localhost/api.php?action=nextsong');
  changeTrack(data.queue[1].title, data.queue[1].artwork, data.queue[1].length, data.queue[1].artist);
}

function requestPause()
{
  var jqxhr = $.getJSON('http://localhost/api.php?action=pause');
}
