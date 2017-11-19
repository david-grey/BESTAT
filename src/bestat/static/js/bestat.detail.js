function drawStacked(arr) {
    var data = google.visualization.arrayToDataTable(arr);

    var options = {
        width: 300,
        height: 180,
        isStacked: true,
        colors: ['#e0440e', '#aaaaaa'],
        legend: {position: "none"},
        annotations: {
            textStyle: {
                fontName: 'Helvetica Neue',
                fontSize: 12,
                color: '#666666',
                opacity: 0.9
            }
        },
        axisTitlesPosition: 'none',
        chartArea:{left:0,top:0,width:'100%',height:'80%'},
        dataOpacity: 0.85,
        hAxis: {
            textStyle: {
                fontName: 'Helvetica Neue',
                color: '#555555',
                fontSize: 12,
            },
            minValue: 0,
            maxValue: 10
        },
    };
    var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
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

            var arr = [
                ['Category', 'Score', {role: 'style'}, {role: 'annotation'}, ''],
                ['Overview', data.overview_score, '#d78c6e', 'Overview', 10 - data.overview_score],
                ['Security', data.security_score, '#a2d683', 'Security', 10 - data.security_score],
                ['Service', data.public_service, '#50a6d7', 'Service', 10 - data.public_service],
                ['Convenience', data.live_convenience, '#d3d788', 'Convenience', 10 - data.live_convenience]
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

function postReview() {
    if ($('#newReviewTxt').val().trim() === "") {
        alert("Please input review content.");
        return;
    }

    $("#reviewForm").submit(function (e) {
        var url = "/bestat/create_review"; // the script where you handle the form input.

        $.ajax({
            type: "POST",
            url: url,
            data: $("#reviewForm").serialize(), // serializes the form's elements.
            success: function (data) {
                $('#newReviewTxt').val("");
                $('#safety').barrating('set', 3);
                $('#convenience').barrating('set', 3);
                $('#public').barrating('set', 3);

                alert("Review success. "); // show response from the php script.
            }
        });

        e.preventDefault(); // avoid to execute the actual submit of the form.
    });
}

function populateList(neighbor_id) {
    $.get("/bestat/get_reviews/" + neighbor_id)
        .done(function (data) {
            console.log("start");
            var list = $("#reviews");
            list.html('');
            //getUpdates();
            for (var i = 0; i < data.posts.length; i++) {
                post = data.posts[i];
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




