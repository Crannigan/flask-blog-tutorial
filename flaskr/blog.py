from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = get_all_posts()
    return render_template('blog/index.html', posts=posts)

@bp.route('/like', methods=("POST", "GET"))
def likePost():
    if(request.method == "GET"):
        abort(404)

    id = request.form['post_id']
    db = get_db()
    post = get_post(id, check_author=False)

    if(g.user is None):
        return str(post['likes'])

    isLiked = is_liked(id)
    newLikes = ((post['likes']-1) if isLiked else (post['likes']+1))
    db.execute(
        'UPDATE post'
        ' SET likes = ?'
        ' WHERE id = ?',
        (newLikes, id)
    )

    exists = like_exists(id)
    if(exists):
        liked = (0 if isLiked else 1)
        db.execute(
            'UPDATE likes'
            ' SET liked = ?'
            ' WHERE post_id = ? and liker_id = ?',
            (liked, id, g.user['id'])
        )
    else:
        db.execute(
            'INSERT INTO likes (post_id, liker_id, liked)'
            ' VALUES (?, ?, ?)',
            (id, g.user['id'], 1)
        )

    db.commit()
    post = get_post(id, check_author=False)
    return str(post['likes'])


@bp.route('/comment', methods=('GET', 'POST'))
def commentPost():
    if(request.method == "GET"):
        abort(404)

    id = request.form['post_id']
    db = get_db()

    num_comments = get_num_comments(id)
    start = (num_comments-5) if (num_comments > 4) else 0
    
    if(g.user is None):
        return str("No user")

    db.execute(
                'INSERT INTO comments (author_id, post_id, comment)'
                ' VALUES (?, ?, ?)',
                (g.user['id'], id, request.form['comment_body'])
            )
    db.commit()

    num_comments = get_num_comments(id)
    start = (num_comments-5) if (num_comments > 4) else 0
    comments = get_comments(id, start, 5)

    return comments


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, likes)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], 0)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.view_post', id=id))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>', methods=('GET', 'POST'))
def view_post(id):
    if request.method == 'POST':
        abort(404)

    post = get_post(id, check_author=False)

    num_comments = get_num_comments(id)
    start = (num_comments-5) if (num_comments > 4) else 0
    comments = get_comments(id, start, 5)

    return render_template('blog/view.html', post=post, comments=comments)


@bp.route('/reset', methods=('POST', 'GET'))
def reset():
    db = get_db()
    db.execute('DELETE FROM comments')
    db.commit()
    posts = get_all_posts()
    return render_template('blog/index.html', posts=posts)


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, likes'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


def get_all_posts():
    db = get_db()
    posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username, likes'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' ORDER BY created DESC'
        ).fetchall()

    return posts


def is_liked(id):
    liked = get_db().execute(
        'SELECT liked'
        ' FROM likes'
        ' WHERE post_id = ? and liker_id = ?',
        (id, g.user['id'])
    ).fetchone()

    if liked is None:
        return False

    return (True if liked['liked'] == 1 else False)


def like_exists(id):
    liked = get_db().execute(
        'SELECT liked'
        ' FROM likes'
        ' WHERE post_id = ? and liker_id = ?',
        (id, g.user['id'])
    ).fetchone()

    if liked is None:
        return False

    return True


def get_comments(id, start, count):
    comments = get_db().execute(
        'SELECT comment_id, author_id, post_id, created, comment'
        ' FROM comments'
        ' WHERE post_id = ?'
        ' LIMIT ?, ?',
        (id, start, count)
    ).fetchall()

    commentDict = {}

    for i in range(0, len(comments)):
        temp = comments[len(comments) - i - 1]
        infoDict = {
            'comment_id': temp['comment_id'],
            'author_id': temp['author_id'],
            'post_id': temp['post_id'],
            'created': temp['created'],
            'comment': temp['comment']
        }
        commentDict[i] = infoDict

    return commentDict


def get_num_comments(id):
    numComments = get_db().execute(
        'SELECT count(*) as numComments'
        ' FROM comments'
        ' WHERE post_id = ?',
        (id,)
    ).fetchone()

    return numComments['numComments']