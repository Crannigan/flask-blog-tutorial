function likePost(post_id) {
    $.ajax({
        url:"/like", //the page containing python script
        type: "post", //request type,
        data: {post_id: post_id},
        success: function(response) {
            $(".like-post-"+post_id).html((response !== '0' ? response : 'No') + ' Like' + (response !== '1' ? 's' : ''));
        },
    });
}