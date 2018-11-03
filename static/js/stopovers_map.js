"use strict"

function myCallBack(){
    let map;
    let infoWindow = new google.maps.InfoWindow();
    let marker;
    const waypoints = [];
    const route = $("#routes").data();      //Get start and end address from user
    let origin = route['start'];
    let destination = route['end'];
    const businesses = new Map;


    $('#link-to-stopover-route').on('click', function(evt) {
        evt.preventDefault();
        $.get('/stopover-route/'+origin+'&'+destination, function(data) {
            for (let stopover of data.stopovers) {
                let latitude = stopover['latitude'];
                let longitude = stopover['longitude'];
                console.log(latitude);
                console.log(longitude);
                let id = stopover['id'];
                let name = stopover['name'];
                let waypoint = new google.maps.LatLng(latitude, longitude);
                businesses.set(id, {'name': name,
                                    'waypoint': waypoint});
            }
            console.log(businesses);
            for (let id of businesses.keys()) {
                waypoints.push({location: businesses.get(id).waypoint,
                                stopover: true,
                                });
            }
            console.log(waypoints);
            createMap();
        })
    })

    //Create Map and call calculate and display route function
    function createMap() {
        map = new google.maps.Map(document.getElementById('map2'), {
                center: {'lat': 37.3766893, 'lng':-122.0349817},
                zoom: 10
            });      
        const directionsService = new google.maps.DirectionsService;
        const directionsDisplay = new google.maps.DirectionsRenderer({map:map,
                                                                    suppressMarkers: true,});
        calculateAndDisplayRoute(directionsService, directionsDisplay);
    };

    //Calculate and Display route
    function calculateAndDisplayRoute(directionsService, directionsDisplay) {
        directionsService.route({           //start, end points and travel mode
            origin: origin,
            destination: destination,
            waypoints: waypoints,
            optimizeWaypoints: true,
            travelMode: 'DRIVING'
        }, function (response, status){     //take response and status from API
            if (status == 'OK') {           
                directionsDisplay.setDirections(response);
                console.log(response);          //delete this line when everything starts working//
                //need to add geocoder for this to work!
                let origin_position;
                let geocoder = new google.maps.Geocoder();
                geocoder.geocode({'address': origin}, function(results, status) {
                    if (status === 'OK') {
                        origin_position = results[0].geometry.location
                    }
                });
                let startMarker = new google.maps.Marker({
                                position: origin_position,
                                title: origin
                                });
                startMarker.setMap(map);
                console.log(startMarker);
                let destination_position;
                geocoder.geocode({'address': destination}, function(results, status) {
                    if (status === 'OK') {
                        destination_position = results[0].geometry.location
                    }
                });
                let endMarker = new google.maps.Marker({
                                position: destination_position,
                                map: map,
                                title: destination
                                });
                for (let id of businesses.keys()) {
                    let name = businesses.get(id)['name'][0];
                    console.log(name);
                    let LatLng = businesses.get(id).waypoint;
                    marker = new google.maps.Marker({
                            position: LatLng,
                            map: map, 
                            title : name                           
                        });

                    //need to add more info to info window
                    let myContent = ('<div id="info-window">' +
                                    '<a href="/business/'+ id +'" id="business-name">' +
                                    name + '</div>'
                                    );  
                    displayMyInfoWindow(marker, map, infoWindow, myContent);  
                }

                //function to open, close and set content of the info window
                function displayMyInfoWindow(marker, map, infoWindow, content) {
                    google.maps.event.addListener(marker, 'click', function () {
                        infoWindow.close();
                        infoWindow.setContent(content);
                        infoWindow.open(map, marker);                        
                    });
                }         
                
            } else {
                alert('Directions request failed due to ' + status);
            }
        });
    };
    
}
