$(function () {
    $(".container").css({opacity: .8});
    $.backstretch(["https://s3.amazonaws.com/bestat/pittsburgh/1.jpg", "https://s3.amazonaws.com/bestat/pittsburgh/2.jpg"], {
        duration: 3000,
        fade: 750
    });
});

$(function () {

    $("#city").autocomplete({
        source: "/bestat/get_all_city/",
        minLength: 3

    });
});
