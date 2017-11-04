function loadReview() {
    var url = '/review';

    $.get(url)
        .done(function (data) {
            var div = $("#reviews-div");
            div.data('max-time', data['max-time']);
            div.html('');
            for (var i = 0; i < data.items.length; i++) {
                var item = data.items[i];
                var new_item = $(item.html);
                new_item.data("review-id", item.id);
                div.append(new_item);
            }
        });
}

function loadRecentReview() {
    var url = '/review/';

    var div = $("#reviews-div");
    var max_time = div.data("max-time");
    $.get(url + max_time)
        .done(function (data) {
            div.data('max-time', data['max-time']);
            for (var i = 0; i < data.items.length; i++) {
                var item = data.items[i];
                var new_item = $(item.html);
                new_item.data("review-id", item.id);
                div.prepend(new_item);
            }
        });
}

function postReview(e) {
    if ($(e.target).className !== 'comment_button') {
        alert('fuck');
        return;
    }

    $.post('/post_review', {'text': $('#newReviewTxt').val()})
        .done(function (data) {
            var new_item = $(data.html);
            $(e.target).parent().parent().append(new_item);
            $('#newReviewTxt').val('').focus();
        });
}

$(document).ready(function () {
    // new review word count
    var max_char = 140;
    var msg_count = $('#count_message');

    msg_count.html(max_char + ' remaining');
    $('#newReviewTxt').keyup(function () {
        msg_count.val(msg_count.val().substring(0, max_char));
        msg_count.html(max_char - $('#newReviewTxt').val().length + ' remaining');
    });

    // Add event-handlers
    // $("#add-btn").click(addItem);
    // $("#item-field").keypress(function (e) { if (e.which == 13) addItem(); } );
    // $("#posts-div").click(viewProfile);
    // $("#posts-div").click(showComment);
    //  $("#posts-div").click(postReview);
    // $("#newPostBtn").click(checkPost)

    // Set up to-do list with initial DB items and DOM data
    loadReview();
    //$("#item-field").focus();

    // Periodically refresh post
    // window.setInterval(loadRecentPost, 5000);

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

