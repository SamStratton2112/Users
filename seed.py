from models import User, Post, Tag, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

Martin = User(first_name='Martin', last_name='Doychev', profile_pic='https://hips.hearstapps.com/hmg-prod/images/cute-cat-photos-1593441022.jpg?crop=0.670xw:1.00xh;0.167xw,0&resize=640:*')
Ilian = User(first_name='Ilian', last_name='Daskolov', profile_pic='https://images.pexels.com/photos/1170986/pexels-photo-1170986.jpeg?auto=compress&cs=tinysrgb&w=600')
Sam = User(first_name='Samantha', last_name='Stratton', profile_pic='https://images.pexels.com/photos/1643457/pexels-photo-1643457.jpeg?auto=compress&cs=tinysrgb&w=600')


post1 = Post(title='Milo', content='Milo is the best.', user_id='1')
post2 = Post(title="Milo's Name", content="Milo's name is actually Small Sir.", user_id='2')
post3 = Post(title='Milo the Cat', content='Milo goes by the name of Small Sir and Milo.', user_id='3')
post4 = Post(title="Milo's Birthday", content='Milo was born in September. He is almost 13.', user_id='3')

tag1 = Tag(tag_name='cute')
tag2 = Tag(tag_name='wild')
tag3 = Tag(tag_name='rude')
tag4 = Tag(tag_name='funny')


db.session.add(Martin)
db.session.add(Ilian)
db.session.add(Sam)
db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)
db.session.add(tag4)

db.session.commit()

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)

db.session.commit()


