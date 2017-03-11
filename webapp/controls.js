// Controls
var play = function(){
    console.log("Boom!")
  }

var stop = function() {
  // body...
}

var backward = function(t) {
  // body...
}

var forward = function(t) {
  requestNextSong();
}

var volume = function(d) {
  if (d === 1) {
    // Volume up
  } else if (d === -1) {
    // Volume down
  }
}



var changeTrack = function(name, art, length, artist) {
  document.getElementById('track_name').textContent = name;
  document.getElementById('track_artist').textContent = artist;
  document.getElementById('track_art').src = art;


  // Track progress in percent
  var progress = 75;
  document.getElementById('track_progress').css('width', valeur+'%').attr('aria-valuenow', valeur);
}
