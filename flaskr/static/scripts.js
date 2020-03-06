function likePost(post_id) {
    $.ajax({
        url:"/"+post_id+"/like", //the page containing python script
        type: "get", //request type,
        success: function(response) {
            $(".blog-posts").html(response);
        },
    });
}