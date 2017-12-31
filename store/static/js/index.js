$(function () {
    $("#back").click(function(event){
        event.preventDefault();
        window.history.go(-1);
    });
    $(".nav-sidebar li").click(function () {
        $(this).siblings("li").removeClass("active");
        $(this).addClass("active");
    });
    $("button[name=seach]").click(function(){
        text = $("input[name=seach_text]").val();
        if(text==""){
            alert("搜索内容不能为空");
            return
        }
        my_ajax.post({
            url: "/seach/",
            data: {
                "keyword": text
            },
            success: function(data){
                if(data["code"] == 200){
                    window.location = "/detail/"+data["number"]+"/"
                }else{
                    alert(data["message"])
                }
            },
            error:function(error){
                alert("网络错误!")
            }
        })
    });
});
