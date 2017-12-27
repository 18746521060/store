$(function () {
    $("#modify").click(function () {
        var old_name = $(this).attr("module_name");
        var new_name = prompt("请输入修改后的名字", old_name);
        if (new_name != null && new_name != "") {
            my_ajax.post({
                url: "/module_manager/",
                data: {
                    "new_name": new_name,
                    "old_name": old_name
                },
                success: function (data) {
                    if (data["code"] == 200) {
                        alert(data["message"]);
                        window.location = "/module_manager/"
                    } else {
                        alert(data["message"])
                    }
                },
                error: function (error) {
                    alert("网络错误!")
                }
            })
        }
    });
    $("#delete").click(function () {
        var goods_count = $(this).attr("goods_count");
        var module_name = $(this).attr("module_name");
        if (goods_count == 0) {
            var r = confirm("您确定要删除吗?");
            if (r == true) {
                my_ajax.post({
                    url: "/delete_module/",
                    data: {
                        "name": module_name
                    },
                    success: function (data) {
                        if (data["code"] == 200) {
                            alert(data["message"]);
                            window.location = "/module_manager/"
                        } else {
                            alert(data["message"])
                        }
                    },
                    error: function (error) {
                        alert("网络错误!")
                    }
                });
            }
        } else {
            alert("该模块下有商品，不能删除!")
        }
    })
})