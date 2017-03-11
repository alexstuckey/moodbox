// moodbox.js

//window.data = {};
window.playing = true;
window.theQueue = [];
window.mood = "";

$(document).ready(function(){

  requestUpdate();

  setInterval(function(){requestUpdate()}, 1000);
  console.log("doc ready");

});

function requestUpdate()
{
  // http://localhost/api.php?action=update
  console.log("requested update");
  var jqxhr = $.getJSON('http://drop.robbie.xyz/fbmoodbox/dummyjson.php',function(d){

    console.log(d);
    handleData(d);
    changeTrack(window.theQueue[0].title, window.theQueue[0].artwork, window.theQueue[0].length, window.theQueue[0].artist, window.mood);

  }).fail(function(e){
    console.log("error (probably invalid JSON)",e)});
}

function handleData(d)
{
  window.theQueue = d.queue;
  window.mood = d.mood;
}

function requestNextSong()
{
  // Remove the first element from theQueue
  window.theQueue.shift();
  changeTrack(window.theQueue[0].title, window.theQueue[0].artwork, window.theQueue[0].length, window.theQueue[0].artist, window.mood);
  // http://localhost/api.php?action=nextsong
  var jqxhr = $.getJSON('http://localhost/api.php?action=nextsong');
}

function requestPause()
{
  var jqxhr = $.getJSON('http://localhost/api.php?action=pause');
}
