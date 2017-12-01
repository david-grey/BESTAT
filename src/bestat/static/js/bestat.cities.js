function init() {
    var $container = $('.masonry');

    $container.imagesLoaded(function () {
        $container.masonry({
            itemSelector: '.item'
        })
    });
};

function name() {
    var _bg3width = $(".city_name").width();
    $(".city_name").css("margin-left", _bg3width * -1 / 2 + "px");
};

$(document).ready(function () {
    init();
    //name();

});
