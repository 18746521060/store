$(function () {
    $("button[name=captcha]").click(function (event) {
        var self = $(this);
        var email = $("input[name=email_address]").val();
        if (email != null || email != "") {
            my_ajax.post({
                url: "/get_captcha/",
                data: {
                    "email": email
                },
                success: function (data) {
                    if(data["code"] == 200){
                        alert(data["message"]);
                        var timeCount = 30;
                        var timer = setInterval(function(){
                            self.attr("disabled","disabled");
                            self.css("cursor","default");
                            self.css("width", "106px");
                            self.text(timeCount);
                            timeCount--;
                            if(timeCount <= 0){
                                self.text("发送验证码");
                                self.removeAttr("disabled");
                                clearInterval(timer);
                                self.css("cursor", "pointer");
                            }
                        }, 1000);
                    }else{
                        alert(data["message"])
                    }
                },
                error: function (error) {
                    alert("error")
                }
            })
        }
    });
    $("button[name=regist]").click(function(event){
        event.preventDefault();
        var username = $("input[name=username]").val();
        var password = $("input[name=password]").val();
        var password_repeat = $("input[name=password_repeat]").val();
        var captcha = $("input[name=captcha]").val();
        if(password!=password_repeat){
            alert("确认密码输入错误");
            return
        }
        my_ajax.post({
            url: '/regist/',
            data: {
                "username": username,
                "password": password,
                "password_repeat": password_repeat,
                "captcha": captcha
            },
            success: function(data){
                if(data["code"] == 200){
                    alert(data["message"]);
                    window.location = "/regist/"
                }else{
                    alert(data["message"])
                }
            },
            error: function(error){
                alert(error)
            }
        })
    })
})