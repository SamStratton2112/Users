from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

Martin = User(first_name='Martin', last_name='Doychev', profile_pic='https://hips.hearstapps.com/hmg-prod/images/cute-cat-photos-1593441022.jpg?crop=0.670xw:1.00xh;0.167xw,0&resize=640:*')
Ilian = User(first_name='Ilian', last_name='Daskolov', profile_pic='https://images.pexels.com/photos/1170986/pexels-photo-1170986.jpeg?auto=compress&cs=tinysrgb&w=600')
Sam = User(first_name='Samantha', last_name='Stratton', profile_pic='https://images.pexels.com/photos/1643457/pexels-photo-1643457.jpeg?auto=compress&cs=tinysrgb&w=600')

db.session.add(Martin)
db.session.add(Ilian)
db.session.add(Sam)

db.session.commit()