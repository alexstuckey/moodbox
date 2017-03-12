// moodbox.js

//window.data = {};
window.playing = true;
window.theQueue = [];
window.mood = "";
window.API_URL = "http://community.dur.ac.uk/mohammed.m.rahman/moodbox/backend/api.php";
window.currentProgress = 0.0;

$(document).ready(function(){

  requestUpdate();

  setInterval(function(){requestUpdate()}, 1000);
  console.log("doc ready");

  setInterval(function(){
    window.currentProgress += 0.2;
    $("#track_progress").css('width', window.currentProgress+'%').attr('aria-valuenow', window.currentProgress);
  }, 30);

});

function requestUpdate()
{
  // http://localhost/api.php?action=update
  console.log("requested update");
  // http://drop.robbie.xyz/fbmoodbox/dummyjson.php
  var jqxhr = $.getJSON(API_URL + '?action=updateUI',function(d){

    console.log(d);
    handleData(d);
    changeTrack(window.theQueue[0].title, window.theQueue[0].artwork_url, window.theQueue[0].length, window.theQueue[0].artist, window.mood);

  }).fail(function(e){
    console.log("error (probably invalid JSON)",e)});
}

function handleData(d)
{
  window.theQueue = d.queue;
  window.mood = d.mood;
}

// function requestNextSong()
// {
//   // http://localhost/api.php?action=nextsong
//   var jqxhr = $.getJSON(API_URL + '?action=next');
// }

function requestPause()
{
  var jqxhr = $.getJSON(API_URL + '?action=pause');
}
