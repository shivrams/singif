"use strict";

$(function() { // upon DOM having loaded

  getSingif("some paramters", function(resp){

    if (resp.status != 200) {
      console.error("Something broke. Status code " + resp.status + ": " + resp.mesg);
    }
    else {
      resp.gifs.forEach(function(gif, i) {
        window.setTimeout(function() {
          $("#drivein").append("<img src='" + gif.url + "'>");
          // calculate ratio and set CSS width OR height to stretch to fit
          // very brief crossfade?
          // delete previous img
        }, gif.ts*100); // *100 for now cause i don't want to wait 21 seconds
      });
    }

  }); // end getSingif()

}); // end upon DOM having loaded

function getSingif(param1, cb) {
  // dummy data:
  cb({
      "status": 200,
      "mesg": "success",
      "meta": {
          "title": "blah",
          "original_url": "http://whatyoupassedin.com"
      },
      "embed": "<iframe width=\"560\" height=\"315\" src=\"//whatyoupassedin.com\" frameborder=\"0\" allowfullscreen></iframe>",
      "lines": [
          {
              "text": "oh yeah",
              "ts": 8
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
              "ts": 14,
              "loops": 4,
              "style": "center"
          }, {
              "url": "http://media.giphy.com/media/cr5u0ZEbQpVPG/giphy.gif",
              "ts": 21,
              "loops": -1,
              "style": "tile"
          }
      ]
  });
}