"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User

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
    profile_url = request.form['profile_url']
    new_user = User(first_name=first_name, last_name=last_name, profile_url=profile_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/details')
def show_user_details(user_id):
    """shows user information"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)
    
@app.route('/users/<int:user_id>/delete', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id = user_id).delete()
    db.session.commit()
    redirect ('/users')

