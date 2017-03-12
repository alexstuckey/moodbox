// moodbox.js

//window.data = {};
window.playing = true;
window.currentlyPlaying = "";
window.theQueue = [];
window.currentTrack = 0;
window.mood = "";
window.API_URL = "http://community.dur.ac.uk/mohammed.m.rahman/moodbox/backend/api.php";
window.currentProgress = 0.0;

$(document).ready(function(){

  requestUpdate();

  setInterval(function(){requestUpdate()}, 1000);

  setInterval(function(){
    window.currentProgress += 0.2;
    if (window.currentProgress > 100) {
      window.currentProgress = 100;
    }
    $("#track_progress").css('width', window.currentProgress+'%').attr('aria-valuenow', window.currentProgress);
  }, 30);

});

function requestUpdate()
{
  // http://localhost/api.php?action=update
  // http://drop.robbie.xyz/fbmoodbox/dummyjson.php
  var jqxhr = $.getJSON(API_URL + '?action=updateUI',function(d){

    handleData(d);
    
    changeTrack(window.theQueue[window.currentTrack].title, window.theQueue[window.currentTrack].artwork_url, window.theQueue[window.currentTrack].length, window.theQueue[window.currentTrack].artist, window.mood);
    
    if (window.currentlyPlaying !== window.theQueue[window.currentTrack].title) {
      window.currentProgress = 0.0;
      window.currentlyPlaying = window.theQueue[window.currentTrack].title;
    }


  }).fail(function(e){
    console.log("error (probably invalid JSON)",e)});
}

function compareQueues(a, b) {
  if (a.length === b.length) {

    for (var i = 0; i < a.length; i++) {
      if ( JSON.stringify(a[i]) !== JSON.stringify(b[i]) ) {
        return false;
      }
    }

    return true;
    

  } else {
    return false;
  }
  
}

function handleData(d)
{
  if (compareQueues(window.theQueue, d.queue)) {
    // Same
  } else {
    // Sever has changed queue – should reset the index counter
    window.theQueue = d.queue;
    window.currentTrack = 0;
    window.mood = d.mood;
  }
  
}

function requestNextSong()
{
  // Update UI


}

function requestPause()
{
  var jqxhr = $.getJSON(API_URL + '?action=pause');
}
