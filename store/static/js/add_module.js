$(function(){
    $("button[name=check_btn]").click(function(event){
        var name = $("input[name=name]").val();
        if(name==""){
            alert("模块名称不能为空!");
            return
        }
        my_ajax.post({
            url: "/check_module_name/",
            data: {
                "name": name
            },
            success: function(data){
                alert(data["message"]);
            },
            error: function(error){
                alert(error)
            }
        })
    });
    $("button[name=add]").click(function(event){
        event.preventDefault();
        var name = $("input[name=name]").val();
        if(name==""){
            alert("模块名称不能为空!");
            return
        }
        my_ajax.post({
            url: "/add_module/",
            data: {
                "name": name
            },
            success: function(data){
                alert(data["message"]);
                window.location = "/add_module/"
            },
            error: function(error){
                alert(error)
            }
        })
    })
})