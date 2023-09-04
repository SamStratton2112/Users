"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post

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
    """send add edited user post request to db and redirect to home page"""
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
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect ('/users')

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content)
    user_id = request.form['user_id']
    db.session.add(new_post)
    db.session.commit()
    user = User.query.get_or_404(user_id)
    post = Post.query.filter(Post.user_id == user_id).all()
    return redirect(f'/users/details/{user_id}')

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.post_user.id)
    return render_template('edit_post.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title= request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/details/{post.post_user.id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')



# My created at isn't working at all 
# I can add new posts but they only show up on my table and no user_id is being 
# associated with them 