var map;
var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var curLocation;

var fadeWheel;
var wheelFade;
var fadeDecision;
var decisionFade;

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
    document.getElementById("transit").innerHTML = Math.ceil(object["response"]["transit_time"] / 60) + " minutes";
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
    xhr.open("GET", "http://fortunefish.tk:5959/api/goto.json/?start_lat=42.3598&start_lon=-71.0921&end_lat=42.3744&end_lon=-71.1169", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            callback_function(JSON.parse(xhr.responseText));
        }
    }
    console.log("guys");
    xhr.send();
    console.log("wtf guys");
}


function calcRoute(destination) {
    console.log("calculating from: " + curLocation + " to: " + destination);

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




