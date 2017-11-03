var mymap;
var popup;
var geojsonFeature = "";

$(document).ready(function () {
    mymap = L.map('mapid').setView([40.43, -79.99], 14);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoiZG9yYWRob3UiLCJhIjoiY2o4a2ZzOTZpMGNwODJ3cGZkbXQzOTFtMCJ9.6e0L2AOL8scVc4XTNao8qw'
    }).addTo(mymap);

    popup = L.popup();
    mymap.on('click', onMapClick);

    loadNeighborLayer();
});

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(mymap);
}

function loadNeighborLayer() {
    $.get('/load_city/Pittsburgh')
    .done(function (data) {
       geojsonFeature = JSON.parse(data);
        alert('get geojson');
        console.log(geojsonFeature);
        L.geoJSON(geojsonFeature).addTo(mymap);
    });
}

// [{"type": "FeatureCollection", "features": []}];



// var popup = L.popup()
//     .setLatLng([40.41190996388554,-79.99898231628832])
//     .setContent("<b>Good place to live</b><br>Education:<br>Salary:<br>Transportation:<br>Crime:")
//     .openOn(mymap);




// mymap.on('mouseover', highlightFeature);
// mymap.on('mouseout', resetHighlight);



function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight
    });
}

// geojson = L.geoJson(geojsonFeature, {
//     //style: style,
//     onEachFeature: onEachFeature
// }).addTo(mymap);
