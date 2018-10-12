"use strict"
const coordinates = [];
let steps;
let map;
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
                for (let i=0; i < steps.length; i++){
                    let distance = parseFloat(steps[i].distance.text);
                    if (distance < 40) {
                        let myItem = {'lat': parseFloat(steps[i].end_location.lat()),
                                        'lng': parseFloat(steps[i].end_location.lng())
                                        };
                        coordinates.push(myItem);
                        index += 1;   
                    } else {
                        let j = 0;
                        while (j < steps[i].lat_lngs.length) {
                            let myItem = {'lat': parseFloat(steps[i].end_location.lat()),
                                            'lng': parseFloat(steps[i].end_location.lng())
                                            };
                            coordinates.push(myItem);
                            index += 1;
                            j = j + 1000;
                        }
                    }
                }
                
                const myJSON = JSON.stringify(coordinates);
                const formInputs = {
                    'myJSON': myJSON
                };
                function show_playgrounds(results) {
                    const playgroundDetails = results;
                    console.log(playgroundDetails);
                    console.log(map);
                    for (let i = 0; i < playgroundDetails.length; i++) {
                        const coords = playgroundDetails[i]['coords'];
                        const latLng = new google.maps.LatLng(coords['latitude'],
                                                              coords['longitude']);
                        const name = playgroundDetails['name'];
                        console.log(map);
                        const marker = new google.maps.Marker({
                            position: latLng,
                            map: map,
                            
                        });
                    }
                }

                $.get('/get-route.json', 
                        formInputs, 
                        show_playgrounds) 

            } else {
                alert('Directions request failed due to ' + status);
            }
        });
    };
    createMap();
}
