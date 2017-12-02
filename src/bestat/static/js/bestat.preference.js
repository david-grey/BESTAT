var rangeSlider = function () {
    var slider = $('.range-slider'),
        range = $('.range-slider__range'),
        value = $('.range-slider__value');

    slider.each(function () {

        value.each(function () {
            var value = $(this).prev().attr('value');
            $(this).html(value);
        });

        range.on('input', function () {
            $(this).next(value).html(this.value);
        });
    });
};

rangeSlider();

$(document).ready(function () {
    /* load preference */
    $.get('/bestat/preference/')
        .done(function (data) {
            for (var key in data) {
                $("input[name=" + key + "]").val(data[key]);
            }
        });

    /* set preference */
    $("#saveBtn").on("click", function () {

        var url = "/bestat/preference/"; // the script where you handle the form input.
        $.ajax({
            type: "POST",
            url: url,
            data: $("#preferenceForm").serialize(), // serializes the form's elements.
            success: function (data) {
                var city = $("input[name='city']").val();
                loadNeighborLayer(city);

            }
        });
    });

    /* reset preference */
    $("#resetBtn").click(function () {
        $("input[class='range-slider__range']").each(function () {
            $(this).val(5);
        });
    });

    //CSRF set-up copied from Django docs
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