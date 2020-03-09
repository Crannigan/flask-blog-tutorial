function likePost(post_id) {
    $.ajax({
        url:"/like", //the page containing python script
        type: "post", //request type,
        data: {post_id: post_id},
        success: function(response) {
            $(".like-post-"+post_id).html(response);
        },
    });
}


function commentMade(post_id)  {
    var commentTXT = $('.new-comment-body').val();
    $.ajax({
        url:"/comment",
        type: "post",
        data: {post_id: post_id, comment_body: commentTXT},
        success: function(response) {
            $(".new-comment-body").val('');
            let i = 0;
            while(response[i] !== undefined || i < 5)  {
                $(".comment-text-num"+i).html(response[i]['comment']);
                i++;
            }
        },
    });
}