function drawStacked(arr) {
    var data = google.visualization.arrayToDataTable(arr);

    var options = {
        width: 300,
        height: 120,

        backgroundColor: {fill: 'transparent'},
        colors: ['#e0440e', '#cecece'],
        legend: {position: "none"},
        annotations: {
            textStyle: {
                fontName: 'Helvetica Neue',
                fontSize: 12,
                color: '#474747',
                opacity: 0.9
            }
        },
        is3D: true,
        axisTitlesPosition: 'none',
        chartArea: {left: 0, top: 0, width: '90%', height: '90%'},
        dataOpacity: 0.85,
        hAxis: {
            textStyle: {
                fontName: 'Helvetica Neue',
                color: '#transparent',
                fontSize: 20,
            },
            minValue: 0,
            maxValue: 10,
            gridlines: {
                count: 0
            }
        },


    };
    let chart = new google.visualization.BarChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

function loadScoreGraph(neighbor_id) {
    $.get('/bestat/get_neighbor_detail/' + neighbor_id)
        .done(function (data) {
            // var arr = [
            //     ['Category', 'Score', {role: 'style'}, {role: 'annotation'}, ''],
            //     ['Overview', data.overview_score, '#f0a577', data.overview_score, 10 - data.overview_score],
            //     ['Security', data.security_score, '#bbf098', data.security_score, 10 - data.security_score],
            //     ['Service', data.public_service, '#56bef0', data.public_service, 10 - data.public_service],
            //     ['Convenience', data.live_convenience, '#ecf09e', data.live_convenience, 10 - data.live_convenience]
            // ];

            let arr = [
                ['Category', 'Score', {role: 'style'}, {role: 'annotation'}],
                ['Overview', data.overview_score, '#00649F', 'Overview'],
                ['Security', data.security_score, '#01AAC1', 'Security'],
                ['Service', data.public_service, '#00DBE7', 'Service'],
                ['Convenience', data.live_convenience, '#97ECC5', 'Convenience']
            ];

            drawStacked(arr);

            $('#neighbor').html(data.neighbor_name);
        });
}

function loadReviewGraph(neighbor_id) {
    $.get('/bestat/get_review_detail/' + neighbor_id)
        .done(function (data) {

            let arr = [
                ['Review', 'number'],
                ['Excellent', data.excellent],
                ['Good', data.good],
                ['OK', data.ok],
                ['Bad', data.bad],
                ['Terrible', data.terrible]
            ];

            drawChart(arr);
        });
}

function drawChart(arr) {
    let data = google.visualization.arrayToDataTable(arr);

    let options = {
        chartArea: {left: 0, top: 0, width: '90%', height: '90%'},
        backgroundColor: {fill: 'transparent'},
        colors: ['#00649F', '#01AAC1', '#00DBE7', '#97ECC5', '#AEECE7']
    };
    let chart = new google.visualization.PieChart(document.getElementById('piechart'));
    chart.draw(data, options);
}

function loadPicture(neighbor, city) {

    $.get('/bestat/get_picture?neighbor=' + neighbor + '&city=' + city)
        .done(function (data) {
            let htmlimg = '<img class="center-block img-responsive" src="' + data.link + '" height=\"350\" >';
            console.log(htmlimg);
            document.getElementById('pic').innerHTML = htmlimg
        });

}

$(function () {
    $('#safety').barrating({
        theme: 'fontawesome-stars',
        initialRating: 1,
        hoverState: true
    });
    $('#convenience').barrating({
        theme: 'fontawesome-stars',
        initialRating: 1,
        hoverState: true
    });
    $('#public').barrating({
        theme: 'fontawesome-stars',
        initialRating: 1,
        hoverState: true
    });
});

function postReview() {
    if($("input[name='is_anonymous']").val().includes('True')) {
        alert("Please log in to write reviews.");
        return false;
    }

    if ($('#newReviewTxt').val().trim() === "") {
        alert("Please input review content.");
        return false;
    } else {
        $.ajax({
            type: "POST",
            url: "/bestat/create_review",
            data: $("#reviewForm").serialize(), // serializes the form's elements.
            success: function (data) {
                if (data.status == 'ok') {
                    $('#newReviewTxt').val("");
                    $('#safety').barrating('set', 1);
                    $('#convenience').barrating('set', 1);
                    $('#public').barrating('set', 1);

                    populateList();
                } else {
                    alert(data.err);
                }
            }
        });
    }
}

function populateList() {
    var neighbor_id = $("input[name='neighbor_id']").val();

    $.get("/bestat/get_reviews/" + neighbor_id)
        .done(function (data) {

            var reviews_div = $("#reviews");
            reviews_div.html(data.html);

            $('.review_safety').barrating({
                theme: 'fontawesome-stars',
                readonly: true
            });
            $('.review_convenience').barrating({
                theme: 'fontawesome-stars',
                readonly: true
            });
            $('.review_public').barrating({
                theme: 'fontawesome-stars',
                readonly: true
            });
        });


}


$(document).ready(function () {
    var neighbor_id = $("input[name='neighbor_id']").val();
    var neighbor = $("input[name='neighbor_name']").val();
    var city = $("input[name='city']").val();
    loadScoreGraph(neighbor_id);
    loadPicture(neighbor, city);
    loadReviewGraph(neighbor_id)
    // Set up to-do list with initial DB items and DOM data
    populateList();

    // CSRF set-up copied from Django docs
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});




