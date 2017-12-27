$(function(){
    $("button[name=add]").click(function(event){
        event.preventDefault();
        var name = $("input[name=name]").val();
        var price = $("input[name=price]").val();
        var number = $("input[name=number]").val();
        var module = $("select[name=module]").val();
        my_ajax.post({
            url: "/add_goods/",
            data: {
                "name": name,
                "price": price,
                "number": number,
                "goods_module": module
            },
            success: function(data){
                alert(data["message"]);
                window.location = "/add_goods/"
            },
            error: function(error){
                alert("网络错误!")
            }
        })
    })
})