from models import User, Post, Tag, PostTag, db, default_image_url
from app import app 

with app.app_context():
    db.drop_all()
    db.create_all()
    
    User.query.delete()
    Post.query.delete()
    Tag.query.delete()
    PostTag.query.delete()
    
    john = User(first_name='john',last_name='Williams',image_url=default_image_url)
    susan = User(first_name='susan',last_name='Hills',image_url=default_image_url)
    yun = User(first_name='yun',last_name='Fang',image_url=default_image_url)

    db.session.add(john)
    db.session.add(susan)
    db.session.add(yun)
    
    db.session.commit()


    tag1 = Tag(name="Fun")
    tag2 = Tag(name="Travel")
    tag3 = Tag(name="Animal")
    tag4 = Tag(name="weather")
    tag5 = Tag(name="Cooking")
    tag6 = Tag(name="Food")

    tags = [tag1,tag2,tag3,tag4,tag5,tag6]
    db.session.add_all(tags)
    db.session.commit()

    post1=Post(title="Spring Break",content="We are going to Florida for Spring Break", user_id=1, tags=[tag1,tag2,tag4])

    post2=Post(title="Cooking Class",content="I just signed up for a cooking class, cause I want to make delicious food myself", user_id=1, tags=[tag1,tag5,tag6])

    post3=Post(title="Sunny",content="It's so nice outside, let's have a picnic", user_id=2, tags=[tag1,tag4,tag6])

    post4=Post(title="Dog",content="I love animal so much, just adopted a puppy", user_id=3, tags=[tag3])

    posts = [post1, post2, post3, post4]
    db.session.add_all(posts)
    db.session.commit()
    