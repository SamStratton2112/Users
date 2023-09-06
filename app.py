"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)
db.create_all()

@app.route('/')
def get_users():
    """redirect to users list home page"""
    return redirect('/users')
    

@app.route('/users')
def list_users():
    """show all users in a list"""
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route('/users/new')
def add_user_form():
    """show add user form"""
    return render_template('create_user.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    """send add user post request to db and redirect to home page"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    profile_pic = request.form['profile_pic']
    new_user = User(first_name=first_name, last_name=last_name, profile_pic=profile_pic)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/edit/<int:user_id>')
def edit_user(user_id):
    """show edit user form"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/edit/<int:user_id>', methods=['POST'])
def add_edited_user(user_id):
    """send edited user post request to db and redirect to home page"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.profile_pic = request.form['profile_pic']
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/details/<int:user_id>')
def show_user_details(user_id):
    """shows user information"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template('details.html', user=user, posts=posts)
    
@app.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """delete user from db"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect ('/users')

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    """show post details"""
    post = Post.query.get_or_404(post_id)
    tags = post.tags_on_posts
    return render_template('post_details.html', post=post, tags=tags)

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """show new post form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """add post to db and redirect to user details to view all posts"""
    title = request.form['title']
    content = request.form['content']
    tag_ids = [(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    user_id = user_id
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    for tag in tags:
        new_post_tag = PostTag(post_id=new_post.id, tag_id=tag.id)
        db.session.add(new_post_tag)
        db.session.commit()
    user = User.query.get_or_404(user_id)
    post = Post.query.filter(Post.user_id == user_id).all()
    return redirect(f'/users/details/{user_id}')

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """show edit post form"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.post_user.id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, user=user, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """add edited post to db for update to post and redirect to user details"""
    post = Post.query.get_or_404(post_id)
    post.title= request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/details/{post.post_user.id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """delete post from db and redirect to all users"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')

@app.route('/tags/<int:tag_id>')
def all_posts_with_tag(tag_id):
    """Show all posts that have the specefied tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts_with_tag
    return render_template('tag_details.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """delete a tag from db and redirect to view all tags"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags')
def show_tags():
    """show all tags"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/new')
def add_tag_form():
    """show add tag form"""
    return render_template('create_tag.html')

@app.route('/tag/new', methods=['POST'])
def add_tag_post_req():
    """send new tag data to db via post request"""
    tag_name = request.form['tag_name_input']
    new_tag = Tag(tag_name=tag_name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """show edit tag form"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def add_edited_tag(tag_id):
    """add edited tag to db and redirect to tags"""
    tag = Tag.query.get_or_404(tag_id)
    tag.tag_name = request.form['tag_name_input']
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')
