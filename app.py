"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "i-am-secret-key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.debug = True
debug = DebugToolbarExtension(app)

connect_db(app)

# with app.app_context():
#     db.create_all()

@app.route('/')
def home_page():
    """home page"""
    return redirect('/users')

@app.route('/users')
def users_page():
    """list of users"""
    users = User.query.all()
    return render_template("users_list.html", users=users)

@app.route('/users/new')
def create_user():
    """show user form"""
    return render_template("new_user_form.html")

@app.route('/users/new', methods=["POST"])
def new_user():
    """create a user"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_URL']

    user = User (first_name=first_name,last_name=last_name,image_url=image_URL)
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user.id)
    return render_template("user_details.html", user=user,posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """edit a user"""
    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html",user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def show_user_after_editing(user_id):
    """show details about a single user after editing"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_URL = request.form['image_URL']
    db.session.add(user)
    db.session.commit()
    return redirect('/')

@app.route('/users/<int:user_id>/delete',methods=['POST'])
def delete_user(user_id):
    """delete a user"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/')

@app.route('/users/<int:user_id>/posts/new')
def add_new_post(user_id):
    """add new post form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("new_post_form.html",user=user,tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def show_new_post(user_id):
    """added a new post"""
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist('name')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post = Post(title=title, content=content, user_id=user_id, tags=tags)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):
    """display a post"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id;
    user = User.query.get_or_404(user_id)
    tags = post.tags
    return render_template('post_details.html',post=post,user=user,tags=tags)

@app.route('/posts/<int:post_id>/edit')
def post_edit_form(post_id):
    """edit a post"""
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    tagList = Tag.query.all()
    return render_template('post_edit_form.html',post=post,tags=tags,tagList=tagList)

@app.route('/posts/<int:post_id>/edit',methods=['POST'])
def show_post_after_editing(post_id):
    """display a edited post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist('name')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post.tags = tags
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete',methods=['post'])
def delete_a_post(post_id):
    """delete a post"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/tags')
def list_tags():
    """list all tags"""
    tags = Tag.query.all()
    return render_template('tag_list.html',tags=tags)

@app.route('/tags/new')
def add_new_tag():
    return render_template('add_new_tag.html')

@app.route('/tags/new', methods=["POST"])
def new_tag_added():
    name = request.form['name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    """show detail about a tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts 
    return render_template('tag_details.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit')
def tag_edit(tag_id):
    """edit a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_edit_form.html',tag=tag)

@app.route('/tags/<int:tag_id>/edit',methods=["POST"])
def update_tag_edit(tag_id):
    """update a tag edit"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """delete a tag"""
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect('/tags')




