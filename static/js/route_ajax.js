"use strict";
let start;
let end;
function assignStartEnd(results) {
    console.log(start, end);
        let result;         //This would have response.routes[0].legs[0].steps latlng data
        console.log('hi');
        function createMap() {
            console.log('there')
            let map = new google.maps.Map(document.getElementById('map'), {
                    center: {lat: 37.38 , lng: -121.94 },
                    zoom: 10
                });
            console.log('hi');
            let directionsService = new google.maps.DirectionsService;
            let directionsDisplay = new google.maps.DirectionsRenderer;
            directionsDisplay.setMap(map);
            calculateAndDisplayRoute(directionsService, directionsDisplay);
        }

        function calculateAndDisplayRoute(directionsService, directionsDisplay) {
            directionsService.route({
                origin: start,
                destination: end,
                travelMode: 'DRIVING'
            }, function (response, status){
                console.log(start, end);
                if (status == 'OK') {
                    directionsDisplay.setDirections(response);
                    result = response;
                } else {
                    window.alert('Directions request failed due to ' + status);
                }
            } );
        }
}


function getRouteInfo(evt) {
    evt.preventDefault();

    var formInputs = {
        "start": $("#start").val(),
        "end": $("#end").val(),
    };

    $.get("/delivery-info.json",
        formInputs,
        assignStartEnd);
}

$("#route-form").on("submit", getRouteInfo);
console.log(start, end);

