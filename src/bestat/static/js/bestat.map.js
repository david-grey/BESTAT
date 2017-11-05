var mymap;
var popup;
var geojson;

$(window).resize(function () {//resize window
    $('#mapid').height($(window).height()-15);
    $('#mapid').width($(window).width()-15);
});

$(document).ready(function () {
    /* set map div size */
    $('#mapid').height($(window).height()-15);
    $('#mapid').width($(window).width()-15);

    /* set city centre coordinate */
    var centre_coordinate = JSON.parse($("input[name='coordinate']").val());
    mymap = L.map('mapid').setView(centre_coordinate, 12);

    /* map tile */
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoiZG9yYWRob3UiLCJhIjoiY2o4a2ZzOTZpMGNwODJ3cGZkbXQzOTFtMCJ9.6e0L2AOL8scVc4XTNao8qw'
    }).addTo(mymap);

    /* popup */
    popup = L.popup();
    // mymap.on('click', onMapClick);

    /* load neighbor layer */
    var city = $("input[name='city']").val();
    loadNeighborLayer(city);

    /* add legend */
    var legend = L.control({position: 'bottomright'});
    legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),
            grades = [0, 200000, 220000, 240000, 260000, 280000, 300000, 320000],
            labels = [];

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML +=
                '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
                grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
        }
        return div;
    };
    legend.addTo(mymap);
});

/**
 * onclick event
 */
function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(mymap);

    geojson.setStyle(changeStyle);
}


function loadNeighborLayer(city) {
    $.get('/bestat/load_city/' + city)
        .done(function (data) {
            // geojsonFeature = [{"type": "FeatureCollection", "features": []}];

            geojson = L.geoJson(data, {
                style: style,
                onEachFeature: onEachFeature
            }).addTo(mymap);
        });
}


function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight
    });
}


function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    var props = layer.feature.geometry.properties;
    var html = '<h4>' + props.name + ' Index</h4>'
        + 'Block id: ' + props.id + '<br/>'
        + 'Random: ' + props.random;

    popup
        .setLatLng(e.latlng)
        .setContent(html)
        .openOn(mymap);

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}


function resetHighlight(e) {
    //geojson.resetStyle(e.target);
    geojson.setStyle({
        weight: 2,
        color: 'white',
        dashArray: '5',
        fillOpacity: 0.7
    })
}


function getColor(d) {
    return d > 320000 ? '#800026' :
           d > 300000 ? '#BD0026' :
           d > 280000 ? '#E31A1C' :
           d > 260000 ? '#FC4E2A' :
           d > 240000 ? '#FD8D3C' :
           d > 220000 ? '#FEB24C' :
           d > 200000 ? '#FED976' :
                        '#FFEDA0';
}


function style(feature) {
    return {
        fillColor: getColor(feature.geometry.properties.random),
        weight: 2,
        opacity: 1,
        color: '#FFF',
        dashArray: '5',
        fillOpacity: 0.7
    };
}


function changeStyle(feature) {
    return {
        fillColor: getColor(feature.geometry.properties.id),
        weight: 2,
        opacity: 1,
        color: '#FFF',
        dashArray: '5',
        fillOpacity: 0.7
    };
}