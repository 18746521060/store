$(function () {
    $("#back").click(function(event){
        event.preventDefault();
        window.history.go(-1);
    });
    $(".nav-sidebar li").click(function () {
        $(this).siblings("li").removeClass("active");
        $(this).addClass("active");
    })
});
