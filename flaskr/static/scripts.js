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

function newComment(id, comment_fields) {
    let comment = document.createElement('div');
    comment.className = ("comment-block comment-num"+id);
    comment.innerHTML = ("<div class='comment-text comment-text-num"+ id +"'>"+ comment_fields['comment'] +"</div>");
    
    if(comment_fields['is_owner'])  {
        comment.innerHTML += (
            "<div class='comment-actions'><div class='edit-comment-button'>Edit</div><div class='reply-comment-button'>Reply</div></div>"
        );
    }   else    {
        comment.innerHTML += (
            "<div class='comment-actions'><div class='reply-comment-button'>Reply</div></div>"
        );
    }

    return comment;
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
            document.getElementsByClassName("comments-body")[0].innerHTML = '';
            while(response[i] !== undefined || i < 5)  {
                let clone = newComment(i, response[i]);
                $(".comments-body")[0].append(clone);
                i++;
            }
        },
    });
}