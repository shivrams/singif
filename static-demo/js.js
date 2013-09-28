"use strict";

var TRANSITION = 250;

$(function() { // upon DOM having loaded
  $("#singif").click(function() {
    var button = $(this);
    if (button.hasClass("pressed")) return;
    button.addClass("pressed"); // to avoid a flicker when you let go
    $("#input").delay(TRANSITION/2).animate({ opacity: 0 }, TRANSITION);
    $("#drivein").css({display: "inline-block"});
    singif(function singifCB() {
      button.removeClass("pressed");
      button.html("let's do it again");
      $("#input").animate({ opacity: 1 }, TRANSITION);
    });
  })
}); // end upon DOM having loaded

function singif(cb) {

  // reset containers in case we've already played something
  $("#gifs").html("<div class='gif'></div><div class='lyric'></div>"); // dummies to make JS easier
  // also reset #yt

  // set loading icon
  
  getSingif("some parameters", function getSingifCB(resp){
    if (resp.status != 200) {
      console.error("Something broke. Status code " + resp.status + ": " + resp.mesg);
    }
    else {
      // schedule gifs
      resp.gifs.forEach(function(gif, i) {
        window.setTimeout(function() {
          $("#gifs").append("<div class='gif' style='background-image: url(" + gif.url + "); display: none;'></div>");
          $($("#gifs .gif")[1]).fadeIn(TRANSITION);
          $($("#gifs .gif")[0]).fadeOut(TRANSITION, function() {
            $(this).remove();
          });
        }, gif.ts*250);
      });

      // schedule lyrics
      resp.lines.forEach(function(line, i) {
        window.setTimeout(function() {
          $("#gifs").append("<div class='lyric'>" + line.text + "</div>");
          $($("#gifs .lyric")[1]).fadeIn(TRANSITION);
          $($("#gifs .lyric")[0]).fadeOut(TRANSITION, function() {
            $(this).remove();
          });
        }, line.ts*250);
      });

      // and for when we're done:
      window.setTimeout(function() {
        cb();
      }, resp.meta.length*250);
    }
  }); // end getSingif()
}

function getSingif(param1, cb) {
  $.getJSON("http://singif.com/api/v1/singif", function(data) {
    cb(data);
  });
}

function getSingifDummy(param1, cb) {
  // dummy data:
  cb({
      "status": 200,
      "mesg": "success",
      "meta": {
          "title": "blah",
          "original_url": "http://whatyoupassedin.com",
          "length": 6
      },
      "embed": "<iframe width=\"560\" height=\"315\" src=\"//whatyoupassedin.com\" frameborder=\"0\" allowfullscreen></iframe>",
      "lines": [
          {
              "text": "oh yeah",
              "ts": 5
          }, {
              "text": "such sweet lyrics",
              "ts": 14
          }, {
              "text": "time to gif it",
              "ts": 21
          }
      ],
      "gifs": [
          {
              "url": "http://media.giphy.com/media/vUw3k6CxJCmnm/giphy.gif",
              "ts": 0,
              "loops": 8,
              "style": "center"
          }, {
              "url": "http://media.giphy.com/media/Jztx4VDq2wJBS/giphy.gif",
              "ts": 2,
              "loops": 4,
              "style": "center"
          }, {
              "url": "http://media.giphy.com/media/cr5u0ZEbQpVPG/giphy.gif",
              "ts": 4,
              "loops": -1,
              "style": "tile"
          }
      ]
  });
}