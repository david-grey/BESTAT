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
    popup = L.popup({closeButton: false});
    // mymap.on('click', onMapClick);

    /* load neighbor layer */
    var city = $("input[name='city']").val();
    loadNeighborLayer(city);

    /* add select */
    var sel = L.control({position: 'topright'});
    sel.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'category');
        div.innerHTML = '<span>EXPLORE THIS AREA: </span><i data-toggle="tooltip" title="Security" class="fa fa-bomb fa-2x"></i><i data-toggle="tooltip" title="Public Services" class="fa fa-institution fa-2x"></i><i data-toggle="tooltip" title="Live Convenient" class="fa fa-shopping-cart fa-2x"></i>';
        return div;
    }
    sel.addTo(mymap);
    $('.fa').click(changeCategory);

    /* add legend */
    var legend = L.control({position: 'bottomright'});
    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend'),
            grades = [0, 2, 4, 6, 8, 10],
            labels = [];

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML +=
                '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
                grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '');
        }
        return div;
    };
    legend.addTo(mymap);

    $('#categorySlt').bind('change',changeCategory);
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


function changeCategory(e) {
    var bg_color = $(this).css('background-color');
    if (bg_color === $('.category').css('background-color')) {
        $('.category').children().css('background-color', '#fff');
        $(this).css('background-color', '#ddd');

        var category = $(this).attr('title');
        console.log(category);
        switch (category) {
            case 'Security':
            case 'Public Services':
                geojson.setStyle(securityStyle);
                break;
            case 'Live Convenient':
                geojson.setStyle(randomStyle);
                break;
        }
    } else {
        $(this).css('background-color', '#fff');
        geojson.setStyle(style);
    }

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
    var html = '<h4>' + props.name + '</h4>'
        + '<span>Overall: ' + props.overview_score + '</span><br/>'
        + '<span>Security: ' + props.security_score + '</span>';

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
    return d >= 10 ? '#BD0026' :
           d > 8 ? '#E31A1C' :
           d > 6 ? '#FC4E2A' :
           d > 4 ? '#FD8D3C' :
           d > 2 ? '#FED976' :
                        '#FFEDA0';
}


function style(feature) {
    return {
        fillColor: getColor(feature.geometry.properties.overview_score),
        weight: 2,
        opacity: 1,
        color: '#FFF',
        dashArray: '5',
        fillOpacity: 0.7
    };
}


function securityStyle(feature) {
    return {
        fillColor: getColor(feature.geometry.properties.security_score),
        weight: 2,
        opacity: 1,
        color: '#FFF',
        dashArray: '5',
        fillOpacity: 0.7
    };
}

function randomStyle(feature) {
    return {
        fillColor: getColor(feature.geometry.properties.random),
        weight: 2,
        opacity: 1,
        color: '#FFF',
        dashArray: '5',
        fillOpacity: 0.7
    };
}