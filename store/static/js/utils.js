var my_ajax = {
    "get": function(args){
        args["method"] = "get";
        this.ajax(args)
    },
    "post": function(args){
        args["method"] = "post";
        this.ajax(args)
    },
    "ajax": function(args){
        this.setup_tool();
        $.ajax(args)
    },
    "setup_tool": function(){
        $.ajaxSetup({
            "beforeSend": function(xhr, setting){
                var csrf_token = $("meta[name=csrf-token]").attr("content");
                xhr.setRequestHeader("X-CSRFToken", csrf_token)
            }
        })
    }
}