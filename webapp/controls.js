// Controls
// var play = function(){
//   var jqxhr = $.getJSON(API_URL + '?action=control&command=pause');
// }
//
// var pause = function() {
//   var jqxhr = $.getJSON(API_URL + '?action=control&command=pause');
// }

var playpause = function(){
  var jqxhr = $.getJSON(API_URL + '?action=control&command=pause');
  console.log("called pause/play (?action=control&command=pause)");
  if(playing){
    playing = false;
    $('.fa-pause').removeClass('fa-pause').addClass('fa-play');
  }else{
    playing = true;
    $('.fa-play').removeClass('fa-play').addClass('fa-pause');
  }
}

var backward = function(t) {
  var jqxhr = $.getJSON(API_URL + '?action=control&command=previous');
  console.log("called previous (?action=control&command=previous)");
  window.currentTrack -= 1;
}

var forward = function(t) {
  var jqxhr = $.getJSON(API_URL + '?action=control&command=next');
  console.log("called next (?action=control&command=next)");
  window.currentTrack += 1;
  changeTrack(window.theQueue[window.currentTrack].title, window.theQueue[window.currentTrack].artwork_url, window.theQueue[window.currentTrack].length, window.theQueue[window.currentTrack].artist, window.mood);
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
