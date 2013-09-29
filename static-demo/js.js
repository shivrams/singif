"use strict";

var TRANSITION = 250;
var SINGIF_API_URL = "http://api.singif.com/api/v1/singif";
var debug = true;

var player; // global variable for YouTube player

// Deferreds, used in $.when() below
var singifDfd = $.Deferred(); // resolves when user starts a singif and we receive singif JSON
var youtubeDfd = $.Deferred(); // resolves when YT API is ready

$(function() { // upon DOM having loaded
  $("#singif").click(function() {
    var button = $(this);
    if (button.hasClass("pressed")) return;
    button.addClass("pressed"); // to avoid a flicker when you let go
    $("#input").delay(TRANSITION/2).animate({ opacity: 0 }, TRANSITION);
    $("#drivein").css({display: "inline-block"});
    singif(function singifCB() {
      // when singif is done playing
      button.removeClass("pressed");
      button.html("let's do it again");
      $("#input").animate({ opacity: 1 }, TRANSITION);
    });
  })
}); // end upon DOM having loaded

function singif(cb) {
  if (debug) console.log("starting singif process");

  // reset containers in case we've already played something
  $("#gifs").html("<div class='gif'></div><div class='lyric'></div>"); // dummies to make JS easier
  // also reset #yt

  // set loading icon
  
  getSingif("some parameters", function getSingifCB(resp){
    if (resp.status != 200) {
      console.error("Something broke. Status code " + resp.status + ": " + resp.mesg);
    }
    else {
      singifDfd.resolve(resp, cb);

      // TODO: start buffering gifs
    }
  });
}

function getSingif(param1, cb) {
  var url = SINGIF_API_URL + "?song_name=" + encodeURIComponent($("#query").val());
  $.getJSON(url, function(resp) {
    if (debug) {
      console.log("singif JSON loaded. response:");
      console.log(resp);
    }
    cb(resp);
  });
}

// ========= youtube shit ========= //

// returns a Deferred we can pass to $.when() that will resolve when the YT iframe API calls onYouTubeIframeAPIReady()
function loadYTapi(){
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

// when singif JSON and youtube API loaded
$.when(singifDfd, loadYTapi()).done(function(singifArgs) {
  var resp = singifArgs[0]; // JSON response containing singif
  var cb = singifArgs[1] // for when youtube video stops playing

  if (debug) console.log("singif JSON and youtube api loaded");

  // set up the player using resp.meta.id
  player = new YT.Player('player', {
    width: '320',
    height: '240',
    videoId: '6okxuiiHx2w',
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
    if (debug) console.log("YT player ready, playing");
    event.target.playVideo();
    playSingif(resp);
  }

  // API calls this function when the player's state changes.
  function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.ENDED) {
      if (debug) console.log("singif finished, calling callback");
      cb();
    }
  }
  // function stopVideo() {
  //   player.stopVideo();
  // }

});

function playSingif(resp) {
  if (debug) console.log("starting to play singif");

  // schedule gifs
  resp.gifs.forEach(function(gif, i) {
    window.setTimeout(function() {
      $("#gifs").append("<div class='gif' style='background-image: url(" + gif.url + "); display: none;'></div>");
      $($("#gifs .gif")[1]).fadeIn(TRANSITION);
      $($("#gifs .gif")[0]).fadeOut(TRANSITION, function() {
        $(this).remove();
      });
    }, gif.ts*750);
  });

  // schedule lyrics
  resp.lines.forEach(function(line, i) {
    window.setTimeout(function() {
      $("#gifs").append("<div class='lyric'>" + line.text + "</div>");
      $($("#gifs .lyric")[1]).fadeIn(TRANSITION);
      $($("#gifs .lyric")[0]).fadeOut(TRANSITION, function() {
        $(this).remove();
      });
    }, line.ts*750);
  });
}