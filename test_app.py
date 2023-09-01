from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    """Tests users view."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test_first_name", last_name='Test_last_name', profile_pic="https://upload.wikimedia.org/wikipedia/commons/2/25/Siam_lilacpoint.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/details/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>User Information</h1>', html)
    
    def test_add_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a User</h1>', html)

    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/edit/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.user.first_name, html)
            

