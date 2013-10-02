"use strict";

var TRANSITION = 250;
var SINGIF_API_URL = "http://api.singif.com/api/v1/singif";
var debug = true;
var timers = []; // array of timeouts (see Timer function below) each corresponding to a gif, so we can pause
var timersPlaying = false;

var EUGENE = "Studies have shown that we like sheep are prone \nTo sure fatal doses of malcontent through osmosis \nBut don't be sympathetic, just pass the anaesthetic \n'Cuz sheep are benign and on the young we will dine \nBurn her pale blue shroud, and tread on her bones \nThe din of the boys club crowd, reveals we've always been clones \nOh this being true you know there's more than just two \nIn the cards are four aces so turn and shoot at twelve paces \nStudies have shown that we like sheep are prone \nTo sure fatal doses of malcontent through osmosis \nBut don't be sympathetic, just pass the antisthetic \n'Cuz sheep are benign and on the young we will dine \nBurn her pale blue shroud, and tread on her bones \nThe din of the boys club crowd, reveals we've always been clones \nOh this being true you know there's more than just two \nSo tie up your laces for the gene pool race of races;"

var player; // global variable for YouTube player

// Deferreds, used in $.when() below
var singifDfd = $.Deferred(); // resolves when user starts a singif and we receive singif JSON
var youtubeDfd = $.Deferred(); // resolves when YT API is ready


// ========== SINGIF INTERFACE LOGIC ========== //

$(function() { // upon DOM having loaded
  $("#singif-go").click(singifButtonPressed);
  $("#query").keyup(function(event){
    // enter key:
    if(event.keyCode == 13) singifButtonPressed();
  });
}); // end upon DOM having loaded

function singifButtonPressed() {
  var button = $(this);
  if (button.hasClass("pressed")) return;
  button.addClass("pressed"); // to avoid a flicker when you let go
  $("#input").delay(TRANSITION/2).animate({ opacity: 0 }, TRANSITION);
  $("#message").delay(TRANSITION/2).fadeOut(TRANSITION); // hide any error message
  $("#singif").css({display: "inline-block"});

  singif($("#query").val(), singifFinished);
}

function resetSingif() {
  // reset containers in case we've already played something
  $("#gifs").html("<div class='gif'></div><div class='lyric'></div>"); // dummies to make JS easier
  // also reset #yt
  timers = [] // clear timers
}

function setLoading() {
  // TODO
}
function unsetLoading() {
  // TODO
}

function singifFinished() {
  button.removeClass("pressed");
  button.html("let's do it again");
  $("#input").animate({ opacity: 1 }, TRANSITION);
}


// ========== SINGIF PREPARATION LOGIC ========== //

function singif(query, cb) {
  if (debug) console.log("starting singif process");

  resetSingif();

  setLoading();

  getSingifJSON(query, function getSingifCB(resp){
    if (resp.error) {
      var errorMessage = "Problem fetching singif. Status code " + resp.status + ", error code " + resp.error.code + ": " + resp.error.mesg; // default error message
      console.log(errorMessage);
      if (resp.error.code == 101) { // song not found
        errorMessage = "Song could not be found - try searching for something else!";
      }
      $("#message").html(errorMessage).fadeIn(TRANSITION);
      cb(); // unhides search bar etc
    }
    else {
      singifDfd.resolve(resp, cb); // resolve this - YT player will start to load and then setupSingifTimers() will be called

      // TODO: start buffering gifs
    }
  });
}

function getSingifJSON(query, cb) {
  // var url = SINGIF_API_URL + "?song_name=" + encodeURIComponent($("#query").val()) + "&song_lyrics=" + encodeURIComponent(EUGENE);
  var url = SINGIF_API_URL + "?song_name=" + encodeURIComponent(query);
  $.getJSON(url, function(resp) {
    if (debug) {
      console.log("singif JSON loaded. response:");
      console.log(resp);
    }
    cb(resp);
  });
}


// ========== YOUTUBE HOOKS AND SHIT ========== //

// returns a Deferred we can pass to $.when() that will resolve when the YT iframe API calls onYouTubeIframeAPIReady()
function loadYouTubeAPI(){
  var dfd = $.Deferred();

  window.onYouTubeIframeAPIReady = function() {
    if (debug) console.log("youtube API ready");
    dfd.resolve(); // resolve with context
  };

  // load the iframe player API code asynchronously
  var tag = document.createElement('script');
  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

  return dfd;
}

// when singif JSON and youtube API are both loaded
$.when(singifDfd, loadYouTubeAPI()).done(function(singifArgs) {
  var resp = singifArgs[0]; // JSON response containing singif
  var cb = singifArgs[1] // for when youtube video stops playing

  if (debug) console.log("singif JSON and youtube api loaded");

  // set up the player using resp.meta.id
  player = new YT.Player('player', {
    width: '320',
    height: '240',
    videoId: resp.meta.id,
    playerVars: {
      'autohide': 1,
      'rel': 0, // don't show related videos when video done. TODO: could add this later, and do a singif for whatever they click on
      'showinfo': 0 // hide titlebar and uploader
    },
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });

  // API calls this when the video player is ready.
  function onPlayerReady(event) {
    if (debug) console.log("YT player ready");
    setupSingifTimers(resp);
    event.target.playVideo(); // autostart playing
    unsetLoading();
  }

  // API calls this function when the player's state changes.
  function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.ENDED) {
      if (debug) console.log("singif finished, calling callback");
      cb();
    }
    else if (event.data == YT.PlayerState.PAUSED || event.data == YT.PlayerState.BUFFERING) {
      if (debug) console.log("YT player paused or buffering");
      pauseTimers();
    }
    else if (event.data == YT.PlayerState.PLAYING) {
      if (debug) console.log("YT player playing");
      resumeTimers();
    }
  }

}); // end $.when()


// ========== TIMING STUFF ========== //

function setupSingifTimers(resp) {
  if (debug) console.log("scheduling singif timers");

  // schedule gifs
  resp.gifs.forEach(function(gif, i) {
    timers.push(new Timer(function() {
      $("#gifs").append("<div class='gif' style='background-image: url(" + gif.url + "); display: none;'></div>");
      $($("#gifs .gif")[1]).fadeIn(TRANSITION);
      $($("#gifs .gif")[0]).fadeOut(TRANSITION, function() {
        $(this).remove();
      });
    }, gif.ts*1000));
  });

  // schedule lyrics
  resp.lines.forEach(function(line, i) {
    timers.push(new Timer(function() {
      $("#gifs").append("<div class='lyric'>" + line.text + "</div>");
      $($("#gifs .lyric")[1]).fadeIn(TRANSITION);
      $($("#gifs .lyric")[0]).fadeOut(TRANSITION, function() {
        $(this).remove();
      });
    }, line.ts*1000));
  });
}


function pauseTimers() {
  if (!timersPlaying) return;
  if (debug) console.log("Pausing singif timers");
  timers.forEach(function(timer) {
    timer.pause();
  });
  timersPlaying = false;
}
function resumeTimers() {
  if (timersPlaying) return;
  if (debug) console.log("Resuming singif timers");
  timers.forEach(function(timer) {
    timer.resume();
  });
  timersPlaying = true;
}

// wrapper for window.setTimeout() that we can pause and resume
// http://stackoverflow.com/a/3969760/458614
function Timer(callback, delay) {
    var timerId, start, remaining = delay;

    this.pause = function() {
        window.clearTimeout(timerId);
        remaining -= new Date() - start;
    };

    this.resume = function() {
        start = new Date();
        timerId = window.setTimeout(callback, remaining);
    };

    // this.resume(); // let's actually not start them automatically
}