"use strict"

function myCallBack(){
    let map;
    let infoWindow = new google.maps.InfoWindow();
    let marker;
    let waypoints;
    let origin, destination;
    const businesses = new Map;
    const routeInfo = new Map;


    $('.link-to-stopover-route').on('click', function(evt) {
        evt.preventDefault();
        waypoints = [];
        businesses.clear();
        
        const route = $(evt.target).data();      //Get start and end address from user
        origin = [route['start'], 'A'];
        destination = [route['end'], 'B'];
        $.get('/stopover-route/'+origin[0]+'&'+destination[0], function(data) {
            for (let stopover of data.stopovers) {
                let latitude = stopover['latitude'];
                let longitude = stopover['longitude'];
                let id = stopover['id'];
                let name = stopover['name'];
                let waypoint = new google.maps.LatLng(latitude, longitude);
                businesses.set(id, {'name': name,
                                    'waypoint': waypoint});
            }
            for (let id of businesses.keys()) {
                waypoints.push({location: businesses.get(id).waypoint,
                                stopover: true,
                                });
            }
            createMap();
        });
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
            origin: origin[0],
            destination: destination[0],
            waypoints: waypoints,
            optimizeWaypoints: true,
            travelMode: 'DRIVING'
        }, function (response, status){     //take response and status from API
            if (status == 'OK') {           
                directionsDisplay.setDirections(response);
                let routeDistance = 0;
                let routeDuration = 0;
                for (let leg of response.routes[0].legs) {
                    routeDuration = routeDuration + leg.duration.value;
                    routeDistance = routeDistance + leg.distance.value;
                }
                let hour = Math.floor(routeDuration/3600);
                let minutes = Math.floor((routeDuration - hour*3600)/60);
                let routeDurationTime = hour + ' hours, ' + minutes + ' minutes'; 

                routeInfo.set('duration', routeDurationTime);
                routeInfo.set('distance', Math.round(routeDistance*0.000621371*100)/100 + ' miles');
                console.log(routeInfo.get('distance'), routeInfo.get('duration'));
                let html = 'This journey is ' + routeInfo.get('distance') + ' and will take ' + routeInfo.get('duration');
                $('#distance-info').html(html);
                //Add origin and destination markers with infowindows that has addresses
                let geocoder = new google.maps.Geocoder();
                for (let item of [origin, destination]) {
                    geocoder.geocode({'address': item[0]}, function(results, status) {
                        if (status === 'OK') {
                            marker = new google.maps.Marker({
                                map: map,
                                position: results[0].geometry.location,
                                title: item[0],
                                label: item[1]
                            });
                            let myContent = ('<div id="info-window">' +
                                            item + '</div>'
                                            );  
                            displayMyInfoWindow(marker, map, infoWindow, myContent);
                        } else {
                            alert('Geocode was not successful for the following reason: ' + status);
                            }
                    });
                }
                for (let id of businesses.keys()) {
                    let name = businesses.get(id)['name'][0];
                    let LatLng = businesses.get(id).waypoint;
                    let service = new google.maps.places.PlacesService($('#place-photos').get(0));
                    const fields_for_id = ['photo'];
                    const request_for_id = {query: name,
                                            fields: fields_for_id,
                                            locationBias: LatLng};

                    service.findPlaceFromQuery(request_for_id, function(results, status) {
                        if (status === google.maps.places.PlacesServiceStatus.OK) {
                            marker = new google.maps.Marker({
                                        position: LatLng,
                                        map: map, 
                                        title : name,                           
                                    });

                            let myPhoto;
                            let myContent;
                            if (results[0].photos != undefined) {
                                myPhoto = results[0].photos[0].getUrl({'maxHeight': 100});
                                myContent = ('<div id="info-window">' +
                                            '<a href="/business/'+ id +'" id="business-name">' +
                                            name + '<br><img src="'+myPhoto+'" class="img-thumbnail" alt="responsive"></div>'
                                            );  
                            } else {
                                myContent = ('<div id="info-window">' +
                                            '<a href="/business/'+ id +'" id="business-name">' +
                                            name + '</div>'
                                            );  

                            }
                            
                            displayMyInfoWindow(marker, map, infoWindow, myContent);  
                        }
                    });           
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
