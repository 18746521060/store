$(function(){
    $("button[name=to_regist]").click(function(event){
        event.preventDefault();
        window.location = "/regist/"
    });
    $("button[name=to_login]").click(function(event){
        event.preventDefault();
        window.location = "/login/"
    });
})