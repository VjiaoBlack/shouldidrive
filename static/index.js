var map;
var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var lat;
var lon;
var curLocation;

var desta;
var destg;

var fadeWheel;
var wheelFade;
var fadeDecision;
var decisionFade;



// Create the XHR object.
function createCORSRequest(method, url) {
  var xhr = new XMLHttpRequest();
  if ("withCredentials" in xhr) {
    // XHR for Chrome/Firefox/Opera/Safari.
    xhr.open(method, url, true);
  } else if (typeof XDomainRequest != "undefined") {
    // XDomainRequest for IE.
    xhr = new XDomainRequest();
    xhr.open(method, url);
  } else {
    // CORS not supported.
    xhr = null;
  }
  return xhr;
}

// Helper method to parse the title tag from the response.
function getTitle(text) {
  return text.match('<title>(.*)?</title>')[1];
}

// Make the actual CORS request.
function makeCorsRequest() {
  // All HTML5 Rocks properties support CORS.
  var url = 'http://updates.html5rocks.com';

  var xhr = createCORSRequest('GET', url);
  if (!xhr) {
    alert('CORS not supported');
    return;
  }

  // Response handlers.
  xhr.onload = function() {
    var text = xhr.responseText;
    var title = getTitle(text);
    alert('Response from CORS request to ' + url + ': ' + title);
  };

  xhr.onerror = function() {
    alert('Woops, there was an error making the request.');
  };

  xhr.send();
}



function getDest(object) {
    desta = object["results"][1]["geometry"]["location"]["lat"];
    destg = object["results"][1]["geometry"]["location"]["lon"];
}

function callback_function(object)  {
    console.log(object["response"]["drive"]);

    document.getElementsByTagName("img")[0].style.opacity = 0;
    if (object["response"]["drive"])
        document.getElementById("decision").innerHTML = "Yes!";
    else
        document.getElementById("decision").innerHTML = "No!";

    decisionFade = 0;
    fadeDecision = setInterval(function() {
        decisionFade += 0.1;
        if (decisionFade > 1) {
            document.getElementById("decision").style.opacity = 1;
            clearInterval(fadeDecision);
        }
        document.getElementById("decision").style.opacity = decisionFade;

    }, 50);

    document.getElementById("temp").innerHTML = object["response"]["weather_destination"]["temp_f"];
    document.getElementById("weather").innerHTML = object["response"]["weather_destination"]["weather"];
    document.getElementById("transit").innerHTML = Math.ceil(object["response"]["travel_time"]["public"]["seconds"] / 60) + " minutes";
}

function shouldIUber() {
    
    wheelFade = 0;
    fadeWheel = setInterval(function() {
        wheelFade+= 0.1;
        if (wheelFade > 1) {
            document.getElementsByTagName("img")[0].style.opacity = 1;
            clearInterval(fadeWheel);
        }
        document.getElementsByTagName("img")[0].style.opacity = wheelFade;

    }, 50);

    var xhr = new XMLHttpRequest();
    xhr.open("GET", "https://maps.googleapis.com/maps/api/geocode/json?address="+document.getElementById("destinationName").innerHTML+"&key=AIzaSyD29P9EOBYU5jdFup0BCzUlizjyzncYS38", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            getDest(JSON.parse(xhr.responseText));
        }
    }
    xhr.send();





    var xhr = new XMLHttpRequest();
    xhr.open("GET", "http://fortunefish.tk:5959/api/goto.json/?start_lat="+lat+"&start_lon="+lon+"&end_lat="+desta+"&end_lon="+destg, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            callback_function(JSON.parse(xhr.responseText));
        }
    }
    xhr.send();
}


function calcRoute(destination) {

  var request = {
    origin:curLocation,
    destination:destination,
    travelMode: google.maps.TravelMode.DRIVING
  };
  directionsService.route(request, function(result, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(result);
    }
  });
}



function initialize() {
    directionsDisplay = new google.maps.DirectionsRenderer();
    var mapOptions = {
        zoom: 14,
        scrollwheel: false
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);

    if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = new google.maps.LatLng(position.coords.latitude,
                                       position.coords.longitude);
            curLocation = pos;
            lat = position.coords.latitude;
            lon = position.coords.longitude;

            var infowindow = new google.maps.InfoWindow({
                map: map,
                position: pos,
                content: 'Current Location'
            });

            map.setCenter(pos);
        }, function() {
            handleNoGeolocation(true);
        });
    } else {
        // Browser doesn't support Geolocation
        handleNoGeolocation(false);
    }

    directionsDisplay.setMap(map);
    console.log('asdf');
}

function handleNoGeolocation(errorFlag) {
  if (errorFlag) {
    var content = 'Error: The Geolocation service failed.';
  } else {
    var content = 'Error: Your browser doesn\'t support geolocation.';
  }

  var options = {
    map: map,
    position: new google.maps.LatLng(60, 105),
    content: content
  };

  var infowindow = new google.maps.InfoWindow(options);
  map.setCenter(options.position);
}

google.maps.event.addDomListener(window, 'load', initialize);




