var mymap;
var popup;
var geojson;
var opacity = 0.8;
var viewport_padding = 0.005;
var service;
var map;
var place_list = [];
var default_radius = 1200;
var places = ['school', 'restaurant', 'cafe', 'church', 'store', 'bank', 'gym', 'hospital'];
var myIcon = new Map();
var showPopup = 1;

$(window).resize(function () {//resize window
    $('#mapid').height($(window).height() - 15);
    $('#mapid').width($(window).width() - 15);
});

$(document).ready(function () {

    $('[data-toggle="popover"]').popover();

    /* set map div size */
    $('#mapid').height($(window).height() - 15);
    $('#mapid').width($(window).width() - 15);

    /* set city centre coordinate */
    var centre_coordinate = JSON.parse($("input[name='coordinate']").val());

    map = new google.maps.Map(document.getElementById('google'), {
        center: {lat: centre_coordinate[0], lng: centre_coordinate[1]},
        zoom: 15
    });
    service = new google.maps.places.PlacesService(map);

    // initial icon
    places.map(function (x) {
        myIcon.set(x, L.icon({
            iconUrl: '/static/icon/' + x + '.png',
            iconSize: [38, 38],
            iconAnchor: [22, 22],
            popupAnchor: [-3, -76]
        }))
    });

    mymap = L.map('mapid', {
        contextmenu: true,
        contextmenuWidth: 140,
        contextmenuItems: [{
            text: 'Find the places nearby:'

        }, '-', {
            text: 'Education',
            callback: function (e) {
                search_place('school', e.latlng)
            }
        }, {
            text: 'Restaurant',
            callback: function (e) {
                search_place('restaurant', e.latlng)
            }
        }, {
            text: 'Cafe',
            callback: function (e) {
                search_place('cafe', e.latlng)
            }
        }, {
            text: 'Hospital',
            callback: function (e) {
                search_place('hospital', e.latlng)
            }
        }, {
            text: 'Bank',
            callback: function (e) {
                search_place('bank', e.latlng)
            }
        }, {
            text: 'Church',
            callback: function (e) {
                search_place('church', e.latlng)
            }
        }, {
            text: 'Store',
            callback: function (e) {
                search_place('store', e.latlng)
            }
        }, {
            text: 'Gym',
            callback: function (e) {
                search_place('gym', e.latlng)
            }
        }, '-', {
            text: 'Clear',
            // icon: 'images/zoom-in.png',
            callback: clear_markers
        }]
    }).setView(centre_coordinate, 12);


    /* map tile */
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1IjoiZG9yYWRob3UiLCJhIjoiY2o4a2ZzOTZpMGNwODJ3cGZkbXQzOTFtMCJ9.6e0L2AOL8scVc4XTNao8qw'
    }).addTo(mymap);

    /* load neighbor layer */
    var city = $("input[name='city']").val();
    loadNeighborLayer(city);
    /* popup */
    popup = L.popup({closeButton: false, className: 'custom-popup'});

    /* add sidebar */
    var sidebar = L.control.sidebar('sidebar').addTo(mymap);

    /* add legend */
    var legend = L.control({position: 'bottomleft'});
    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend'),
            grades = [0, 1, 2, 3, 4, 5, 6, 7, 8],
            labels = [];

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = grades.length - 1; i >= 0; i--) {
            var s = '';
            if (i === grades.length - 1) {
                s = 'better';
            } else if (i === 0) {
                s = 'worse';
            }

            div.innerHTML +=
                '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' + s + '<br>';
        }
        return div;
    };
    legend.addTo(mymap);
    var zillow = L.control({position: 'bottomright'});
    zillow.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'zillow');
        div.innerHTML += '<a href="https://www.zillow.com/howto/api/neighborhood-boundaries.htm"><img src="https://www.zillowstatic.com/vstatic/64dd1c9/static/logos/Zillow_Logo_HoodsProvided_RightAligned.gif" ></a>';
        return div;
    };
    zillow.addTo(mymap);

    $('#categorySlt').bind('change', changeCategory);
    $("ul#category").on("click", "li", function () {
        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
            geojson.setStyle(allStyle);
        } else {
            $(this).parent().children().removeClass('active');
            $(this).addClass('active');

            var category = $(this).attr('class');
            switch (category) {
                case 'security active':
                    geojson.setStyle(securityStyle);
                    break;
                case 'services active':
                    geojson.setStyle(publicStyle);
                    break;
                case 'convenience active':
                    geojson.setStyle(liveStyle);
                    break;
            }
        }
    });
    swal({
        title: 'Right click can search nearby-place.',
        html: $('<div>'),
        animation: true,
        customClass: 'animated tada',
        type: "success",
        confirmButtonText: 'Got it!'
    })
});

function changeCategory(e) {
    var bg_color = $(this).css('background-color');
    if (bg_color === $('.category').css('background-color')) {
        $('.category').children().css('background-color', '#fff');
        $(this).css('background-color', '#ddd');

        var category = $(this).attr('title');
        switch (category) {
            case 'Security':
                geojson.setStyle(securityStyle);
                break;
            case 'Public Services':
                geojson.setStyle(publicStyle);
                break;
            case 'Live Convenience':
                geojson.setStyle(liveStyle);
                break;
        }
    } else {
        $(this).css('background-color', '#fff');
        geojson.setStyle(allStyle);
    }
}


function loadNeighborLayer(city) {
    $('#mapid').waitMe({effect: 'roundBounce', bg: 'rgba(255,255,255,0.5)'});

    $.get('/bestat/load_city/' + city)
        .done(function (data) {
            if (geojson != null) {
                geojson.clearLayers();
            }
            // geojsonFeature = [{"type": "FeatureCollection", "features": []}];
            geojson = L.geoJson(data.map_data, {
                style: allStyle,
                onEachFeature: onEachFeature
            }).addTo(mymap);

            loadRecommendation(data.recommendation);
            $('#mapid').waitMe("hide");
        });

}

function loadRecommendation(blocks) {
    var city = $("input[name='city']").val();
    var div = $("div[id='recoBlocks']");
    div.empty();
    for (var i = 0; i < blocks.length; i++) {
        loadBlockPicture(blocks[i], city, div);
    }
}

function loadBlockPicture(neighbor, city, div) {
    $.get('/bestat/get_picture?neighbor=' + neighbor.name + '&city=' + city)
        .done(function (data) {
            div.prepend("<div>\n" +
                "<h4><a href='/bestat/detail/" + neighbor.id + "'>" + neighbor.name + "</a></h4>\n" +
                "<img src='" + data.link + "' width='320px' height='180px'>\n" +
                "</div>");
        });
}

function goToDetail(e) {
    var layer = e.target;
    var props = layer.feature.geometry.properties;
    window.location.href = "/bestat/detail/" + props.id;
}


function onEachFeature(feature, layer) {
    layer.on({
        // mouseover: highlightFeature,
        mouseout: resetHighlight,
        mousemove: highlightFeature,
        click: goToDetail
    });
}


function highlightFeature(e) {
    if (showPopup == 0) {
        return;
    }

    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: opacity
    });

    var props = layer.feature.geometry.properties;
    var html = '<h4>' + props.name + '</h4>'
        + '<span>Overall: ' + props.overview_score + '</span><br/>'
        + '<span>Security: ' + props.security_score + '</span><br/>'
        + '<span>Public Services: ' + props.public_service + '</span><br/>'
        + '<span>Live Convenience: ' + props.live_convenience + '</span>';

    popup
        .setLatLng(e.latlng)
        .setContent(html)
        .openOn(mymap);

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}


function resetHighlight(e) {
    if (showPopup == 0) {
        return;
    }

    //geojson.resetStyle(e.target);
    geojson.setStyle({
        weight: 2,
        color: 'white',
        dashArray: '5',
        fillOpacity: opacity
    });

    // if () {
    //     popup.remove();
    // }
}

function getColor(d) {
    return d > 8 ? '#83d08c' :
        d > 7 ? '#9bce7e' :
            d > 6 ? '#b9cc90' :
                d > 5 ? '#d3d986' :
                    d > 4 ? '#f5e488' :
                        d > 3 ? '#f5cf73' :
                            d > 2 ? '#F4BE78' :
                                d > 1 ? '#f1a971' :
                                    '#e99f74';
}

var default_style = {
    fillColor: 'blue',
    weight: 2,
    opacity: 1,
    color: '#FFF',
    dashArray: '5',
    fillOpacity: opacity
};


function allStyle(feature) {
    default_style['fillColor'] = getColor(feature.geometry.properties.overview_score);
    return default_style;
}

function securityStyle(feature) {
    default_style['fillColor'] = getColor(feature.geometry.properties.security_score);
    return default_style;
}

function publicStyle(feature) {
    default_style['fillColor'] = getColor(feature.geometry.properties.public_service);
    return default_style;
}

function liveStyle(feature) {
    default_style['fillColor'] = getColor(feature.geometry.properties.live_convenience);
    return default_style;
}

function search_place(type, latlng) {
    clear_markers();

    service.nearbySearch({
        location: latlng,
        radius: default_radius,
        type: [type]
    }, function (results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            results.map(function (place) {
                var temp_marker = L.marker([place.geometry.location.lat(), place.geometry.location.lng()], {
                    opacity: 0.8,
                    bounceOnAdd: true,
                    icon: myIcon.get(type)
                });
                temp_marker.addTo(mymap).bindPopup(L.popup({
                    closeButton: false,
                    className: 'custom-popup'
                }).setContent(place.name));
                place_list.push(temp_marker);
            });


            let viewport = results.map(a => a.geometry.viewport).reduce(function (x, y) {
                x.b.b = Math.min(x.b.b, y.b.b);
                x.b.f = Math.max(x.b.f, y.b.f);
                x.f.b = Math.min(x.f.b, y.f.b);
                x.f.f = Math.max(x.f.f, y.f.f);
                return x;
            });
            // console.log(viewport);
            console.log([viewport.f.f, viewport.f.b, viewport.b.b, viewport.b.f]);
            // console.log([(viewport.f.f+viewport.f.f.b)/2,(viewport.b.b+viewport.b.f)/2]);

            let bounds = L.latLngBounds([viewport.f.b - viewport_padding, viewport.b.b - viewport_padding],
                [viewport.f.f + viewport_padding, viewport.b.f + viewport_padding]);
            mymap.flyToBounds(bounds);

        }
    });
}

function clear_markers() {
    place_list.map(function (marker) {
        marker.remove();
    });
    place_list = [];
}
