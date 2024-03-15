"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy 
import datetime 

db = SQLAlchemy()

default_image_url = "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg?auto=compress&cs=tinysrgb&w=800"

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = default_image_url )
    
    posts = db.relationship("Post", backref='user',cascade="all,delete-orphan")

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    create_at = db.Column(db.DateTime, nullable = False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # user = db.relationship('User', backref='posts')
    tags = db.relationship('Tag',secondary='postTags', backref='posts')

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)

class PostTag(db.Model):
    __tablename__ = 'postTags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True) 

