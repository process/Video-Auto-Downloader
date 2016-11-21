// ==UserScript==
// @name        Video Auto-downloader
// @namespace   png-vid-archive
// @description Downloads every viewed youtube video
// @include     http*://*youtube.com/watch?v=*
// @include     http*://*youtube.com/embed/*
// @include     http*://vimeo.com/*
// @version     1.33.7
// @grant       unsafeWindow
// @grant       GM_xmlhttpRequest
// ==/UserScript==

/* XXX TODO
 To remove dependence on ytcenter,
 we gotta hook into onYoutubePlayerReady,
 and call any other callbacks if they exist,
 and save the api for ourselves.
 (This is how ytcenter does it (y) */

console.log("[Auto-download] Youtube Auto-dowloader loading");

function sendPage(uri) {
  uri = uri || unsafeWindow.document.location;

  GM_xmlhttpRequest({
    method: 'GET',
    url: 'http://localhost:8080/dlvid?url=' + escape(uri)
  });
  
  // Old XHR code. Used to work... even though it shouldn't have
  // because of cross-origin issues
  // Unsafe window shit used to magically work too. ~WEIRD~
  //var xhr = new XMLHttpRequest();
  //xhr.open('GET', 'http://localhost:8080/dlvid?url=' + escape(uri));
  //xhr.send();
  
  console.log("[Auto-download] Sent request for " + uri);
}

function getURLFromPlayer(player) {
  var currentVid = player.getVideoUrl();
  
  // Remove stupid timestamp
  currentVid = currentVid.replace(/t=[0-9]*&/, "");
  
  return currentVid;
}

if (window.top == window.self) {
  console.log("[Auto-download] Sending Youtube page");
  sendPage();
} else if (window.location.toString().search('/embed/') > 0) {
  var player;
  var currentVid;
  var pageSent = false;
  
  console.log("[Auto-download] Detected embed");
  
  // Delay 1 second for api to ready up
  setTimeout(function () {
    if (!player) player = unsafeWindow.ytcenter.player.getAPI();
    currentVid = getURLFromPlayer(player)
    console.log("[Auto-download] Embed video detected: " + currentVid);
  
    var id = setInterval(function () { 
      // Send that shit if we watch it
      if (!pageSent && player.getPlayerState() == 1) {
        sendPage(currentVid);
        pageSent = true;
      }

      // Handle changed vid
      var newURL = getURLFromPlayer(player);
      if (currentVid != newURL) {
        currentVid = newURL;
        pageSent = false;
      }
      
    }, 1000);
  }, 1000);
}
