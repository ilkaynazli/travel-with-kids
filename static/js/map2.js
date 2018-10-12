"use strict"
const coordinates = [];
let steps;
let map;
let marker;
const markers = [];
const contentString = new Map();
function myCallBack(){
    const route = $("#map").data()
    const start = route['start'];
    const end = route['end'];

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

    function calculateAndDisplayRoute(directionsService, directionsDisplay) {
        directionsService.route({
            origin: start,
            destination: end,
            travelMode: 'DRIVING'
        }, function (response, status){
            if (status == 'OK') {
                directionsDisplay.setDirections(response);
                console.log(response);
                const myRoute = response;
                steps = myRoute.routes[0].legs[0].steps;
                let index = 0;
                let totalDistance = 0;
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
                const myJSON = JSON.stringify(coordinates);
                const formInputs = {
                    'myJSON': myJSON
                };

                let infowindow = new google.maps.InfoWindow(); 

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
                            name : name                           
                        });
                        markers.push(marker);              
                    }
                }

                $.get('/get-route.json', 
                        formInputs, 
                        show_playgrounds)
                
                for (marker of markers) {
                    $(marker).on('click', function() {
                        infowindow.setContent('<div id="info-window">' + name + '</div>');
                        infowindow.open(map, marker)                    
                    });  
                }        

            } else {
                alert('Directions request failed due to ' + status);
            }
        });
    };
    createMap();
}
