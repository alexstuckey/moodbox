// Controls
var play = function(){
    if(playing)
    {
      var jqxhr = $.getJSON(API_URL + '?action=control&command=pause');
      playing = false;
    }else {
      var jqxhr = $.getJSON(API_URL + '?action=control&command=play');
      playing = true;
    }
  }

var stop = function() {
  // body...
}

var backward = function(t) {
  var jqxhr = $.getJSON(API_URL + '?action=control&command=previous');
}

var forward = function(t) {
  //requestNextSong();
  var jqxhr = $.getJSON(API_URL + '?action=control&command=next');
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

}
