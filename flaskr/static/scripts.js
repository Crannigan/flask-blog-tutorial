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
    console.log(commentTXT);
    console.log(post_id);
    $.ajax({
        url:"/comment", //the page containing python script
        type: "post", //request type,
        data: {post_id: post_id},
        success: function(response) {
            console.log(response);
        },
    });
}