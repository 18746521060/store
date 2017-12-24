$(function () {
    $(".nav-sidebar li").click(function () {
        $(this).siblings("li").removeClass("active");
        $(this).addClass("active");
    })
})