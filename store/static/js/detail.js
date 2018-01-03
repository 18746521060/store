$(function () {
    var status = false;
    var name = $("input[name=name]");
    var price = $("input[name=price]");
    var number = $("input[name=number]");
    var module = $("select[name=module]");
    var remarks = $("textarea[name=remarks]");

    var name_val, price_val, number_val, module_val, remarks_val;
    $("button[name=modify]").click(function (event) {
        status = !status;
        if (status) {
            remove_disabled($(this));
            name_val = name.val();
            price_val = price.val();
            number_val = number.val();
            module_val = module.val();
            remarks_val = remarks.val();
        } else {
            var new_name_val = name.val();
            var new_price_val = price.val();
            var new_number_val = number.val();
            var new_module_val = module.val();
            var new_remarks_val = remarks.val();
            if (name_val == new_name_val &&
                price_val == new_price_val &&
                number_val == new_number_val &&
                module_val == new_module_val &&
                remarks_val == new_remarks_val) {
                alert("没有数据改变，无需修改!")
            } else {
                console.log("come in");
                my_ajax.post({
                    url: "/detail_goods/",
                    data: {
                        "old_number": number_val,
                        "name": new_name_val,
                        "price": new_price_val,
                        "number": new_number_val,
                        "module": new_module_val,
                        "remarks": new_remarks_val
                    },
                    success: function (data) {
                        alert(data["message"])
                    },
                    error: function (error) {
                        alert("网络错误!")
                    }
                })
            }
            set_disabled($(this));

        }
    });
    $("button[name=delete]").click(function () {
        status = false;
        // window.location.reload();
        var number = $("input[name=number]").val();
        var name = $("input[name=name]").val();
        var r = confirm("您确定要删除吗?");
        if (r == true) {
            my_ajax.post({
                url: "/delete_goods/",
                data: {
                    "name": name,
                    "number": number
                },
                success: function (data) {
                    if (data["code"] == 200) {
                        alert(data["message"]);
                        window.location = "/goods_manager/"
                    } else {
                        alert(data["message"])
                    }
                },
                error: function (error) {
                    alert("网络错误!")
                }
            });
        }
    });


    function set_disabled(btn) {
        name.attr("disabled", "disabled");
        price.attr("disabled", "disabled");
        number.attr("disabled", "disabled");
        module.attr("disabled", "disabled");
        remarks.attr("disabled", "disabled");
        btn.text("修改");
    }

    function remove_disabled(btn) {
        name.removeAttr("disabled");
        price.removeAttr("disabled");
        number.removeAttr("disabled");
        module.removeAttr("disabled");
        remarks.removeAttr("disabled");
        btn.text("确定");
    }
})