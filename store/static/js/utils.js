my_ajax = {
    "get": function(args){
        args["method"] = "get";
        self.ajax(args)
    },
    "post": function(args){
        args["method"] = "post";
        self.ajax(args)
    },
    "ajax": function(args){
        self.setup_tool();
        $.ajax(args)
    },
    "setup_tool": function(){
        $.ajaxSetup({
            "beforeSend": function(xhr, setting){
                var csrf_token = $("input[name=scrf_token]").attr("content");
                xhr.setRequestHeader("X-CSRFToken", csrf_token)
            }
        })
    }
}