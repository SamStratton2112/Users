"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy 


db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__='users'

    def __repr__(self):
        u = self
        return f'<User ID ={u.id}, First Name={u.first_name}, Last Name={u.last_name}>'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(20),
                    nullable=False,
                    unique=True)
    last_name = db.Column(db.String(20),
                    nullable=False,
                    unique=True)
    profile_pic = db.Column(db.String(500),
                    nullable=False,
                    unique=True)
    
    def update_info(self, first_name, last_name, profile_pic):
        """Update information for a user """
        self.first_name = first_name
        self.last_name = last_name
        self.profile_pic = profile_pic


class Post(db.Model):
    __tablename__='posts'
    def __repr__(self):
        p= self
        return f'<Title: {p.title}, Created at: {p.created_at}, User: {p.post_user.first_name} {p.post_user.last_name}, Id:{p.id}>'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True,
                    unique=True,
                    nullable=False)
    title = db.Column(db.String(50),
                    nullable=False)
    content = db.Column(db.String(300),
                    nullable=False)
    created_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    post_user = db.relationship('User', backref='posts')

    tags_on_posts = db.relationship('Tag', secondary='post_tag', backref='posts_with_tag')

class Tag(db.Model):
    __tablename__='tags'
    def __repr__(self):
        t= self
        return f'<Id:{t.id}, Name: {t.tag_name}>'
    
    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True,
                    unique=True,
                    nullable=False)
    tag_name = db.Column(db.String(30),
                    nullable=False,
                    unique=True)

class PostTag(db.Model):
    __tablename__='post_tag'
    def __repr__(self):
        pt= self
        return f'<Post ID: {pt.post_id}, Tag Id:{pt.id}>'
    
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'), 
                        primary_key=True, 
                        nullable=False)
    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id'), 
                        primary_key=True, 
                        nullable=False)


    
