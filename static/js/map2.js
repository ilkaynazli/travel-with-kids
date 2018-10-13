"use strict"
function myCallBack(){
    const route = $("#map").data()      //Get start and end address from user
    let map;

    //Create Map and call calculate and display route function
    function createMap() {
        map = new google.maps.Map(document.getElementById('map'), {
                center: {lat: 37.38 , lng: -121.94 },
                zoom: 10
            });      
        const directionsService = new google.maps.DirectionsService;
        const directionsDisplay = new google.maps.DirectionsRenderer;
        directionsDisplay.setMap(map);
        calculateAndDisplayRoute(directionsService, directionsDisplay);
    };

    //Calculate and Display route
    function calculateAndDisplayRoute(directionsService, directionsDisplay) {
        directionsService.route({           //start, end points and travel mode
            origin: route['start'],
            destination: route['end'],
            travelMode: 'DRIVING'
        }, function (response, status){     //take response and status from API
            if (status == 'OK') {           
                directionsDisplay.setDirections(response);
                console.log(response);          //delete this line when everything starts working//
                const myRoute = response;
                const steps = myRoute.routes[0].legs[0].steps;  //take each step of your route 
                let totalDistance = 0;
                const coordinates = [];
                //go through each step and each array the steps have.
                //calculate the distance between each lat_lngs and add it to the total distance
                //when the total distance is > 40000 meters add the final lat_lng to the coordinates array
                //then 0 the total distance and continue until you reach the end point
                for (let i=0; i < steps.length; i++){
                    for (let j=0; j < (steps[i].lat_lngs.length-1); j++) {
                        let distance = google.maps.geometry.spherical.computeDistanceBetween(steps[i].lat_lngs[j], steps[i].lat_lngs[j+1]);
                        totalDistance += distance;
                        if (totalDistance > 40000) {
                            let myItem = {'lat': parseFloat(steps[i].lat_lngs[j+1].lat()),
                                        'lng': parseFloat(steps[i].lat_lngs[j+1].lng())
                                        };
                            coordinates.push(myItem);
                            totalDistance = 0;
                        }
                    }  
                };

                const formInputs = {
                    'myJSON': JSON.stringify(coordinates)
                };

                let marker;
                let infoWindow = new google.maps.InfoWindow();
                let myContent;

                function show_playgrounds(results) {
                    const playgroundDetails = results;
                    for (let i = 0; i < playgroundDetails.length; i++) {
                        const coords = playgroundDetails[i]['coords'];
                        const latLng = new google.maps.LatLng(coords['latitude'],
                                                              coords['longitude']);
                        const name = playgroundDetails[i]['name'];
                        marker = new google.maps.Marker({
                            position: latLng,
                            map: map, 
                            title : name                           
                        });
                        myContent = '<div id="info-window">My Info Window</div>';  
                        displayMyInfoWindow(marker, map,infoWindow, myContent);           
                    }
                }

                $.get('/get-route.json', 
                        formInputs, 
                        show_playgrounds)
                
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
    createMap();
}
