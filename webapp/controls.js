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
  // body...
}

var volume = function(d) {
  if (d === 1) {
    // Volume up
  } else if (d === -1) {
    // Volume down
  }
}



var changeTrack = function(name, art, length) {
  document.getElementById('track_name').textContent = name;
  document.getElementById('track_art').src = art;
}