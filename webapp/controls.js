// Controls
var play = function(){
    if(playing)
    {
      var jqxhr = $.getJSON(API_URL + '?action=pause');
      playing = false;
    }else {
      var jqxhr = $.getJSON(API_URL + '?action=play');
      playing = true;
    }
  }

var stop = function() {
  // body...
}

var backward = function(t) {
  var jqxhr = $.getJSON(API_URL + '?action=previous');
}

var forward = function(t) {
  //requestNextSong();
  var jqxhr = $.getJSON(API_URL + '?action=next');
}

var volume = function(d) {
  if (d === 1) {
    // Volume up
  } else if (d === -1) {
    // Volume down
  }
}



var changeTrack = function(name, art, length, artist, mood) {
  document.getElementById('track_name').textContent = name;
  document.getElementById('track_artist').textContent = artist;
  document.getElementById('track_art').src = art;
  document.getElementById('mood_label').textContent = mood;

  // Track progress in percent
  var progress = 75;
  //document.getElementById('track_progress').css('width', progress+'%').attr('aria-valuenow', progress);
}
