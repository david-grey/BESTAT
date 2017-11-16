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

$(document).ready(function () {
    // Load the Visualization API and the corechart package.
    google.charts.load('current', {'packages': ['corechart']});

    var neighbor_id = $("input[name='neighbor_id']").val();
    loadScoreGraph(neighbor_id);
});



