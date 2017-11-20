function drawStacked(arr) {
    var data = google.visualization.arrayToDataTable(arr);

    var options = {
        width: 400,
        height: 240,
        isStacked: true,
        hAxis: {
            minValue: 0,
            maxValue: 10
        },
        colors: ['#e0440e', 'grey'],
        legend: {position: "none"},
    };
    var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

function loadScoreGraph(neighbor_id) {
    $.get('/bestat/get_neighbor_detail/' + neighbor_id)
        .done(function (data) {
            var arr = [
                ['Category', 'Score', {role: 'style'}, {role: 'annotation'}, ''],
                ['Overview', data.overview_score, '#eba275', data.overview_score, 10 - data.overview_score],
                ['Security', data.security_score, '#9bce7e', data.security_score, 10 - data.security_score],
                ['Public Service', data.public_service, '#4e93c5', data.public_service, 10 - data.public_service],
                ['Convenience', data.live_convenience, '#e8ec9a', data.live_convenience, 10 - data.live_convenience]
            ];

            drawStacked(arr);

            $('#neighbor').html(data.neighbor_name);
        });
}

$(function () {
    $('#safety').barrating({
        theme: 'fontawesome-stars',
        initialRating: 3,
        hoverState: true
    });
    $('#convenience').barrating({
        theme: 'fontawesome-stars',
        initialRating: 3,
        hoverState: true
    });
    $('#public').barrating({
        theme: 'fontawesome-stars',
        initialRating: 3,
        hoverState: true
    });
});

function postReview() {

}

function populateList(neighbor_id) {
    $.get("/bestat/get_reviews/" + neighbor_id)
        .done(function (data) {
            console.log("start");
            var list = $("#reviews");
            list.html('');
            //getUpdates();
            for (var i = 0; i < data.posts.length; i++) {
                revies = data.posts[i];
                var new_post = $(post.html);
                new_post.data("post-id", post.id);
                list.prepend(new_post);
            }

        });
}


$(document).ready(function () {
    var neighbor_id = $("input[name='neighbor_id']").val();
    loadScoreGraph(neighbor_id);
    // Set up to-do list with initial DB items and DOM data
    populateList(neighbor_id);

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




