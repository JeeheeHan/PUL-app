"""TEST Server:

"""
import os
from unittest import TestCase

from server import app,socketio
from model import db,connect_to_db


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_login(self):
        """Test important page."""
        result = self.client.get("/login")
        self.assertIn(b"<h2>Login here</h2>", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '42'

            result = self.client.get("/logout")

            self.assertNotIn(b'user_id', sess)


def example_data():
    """Create some sample data."""

    User.query.delete()
    General_chat.query.delete()
    NLP.query.delete()

    ab = General_chat(message="testing", 
                                userID=1,
                                timestamp="2021-05-03T05:35:04Z")
    cd = General_chat(message="testing2", 
                                userID=2,
                                timestamp="2021-05-03T05:35:04Z")
    ef = General_chat(message="testing3", 
                                userID=3,
                                timestamp="2021-05-03T05:35:04Z")

    leonard = User(username='Leonard')
    liz = User(username='liz')
    maggie = User(username='maggie')
    nadine = User(username='nadine')

    t1= NLP(userID=1,word_count= 1,
                        polarity=0.0,
                        filtered_words="testing",
                        chatID=1)
    t2= NLP(userID=2,word_count= 1,
                        polarity=0.0,
                        filtered_words="testing2",
                        chatID=2)
    t3= NLP(userID=3,word_count= 1,
                        polarity=0.0,
                        filtered_words="testing3",
                        chatID=3)


    db.session.add_all([ab, cd, ef, leonard, liz, maggie, nadine, t1, t2, t3])
    db.session.commit()

class FlaskTestDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING']=True
        app.config['SECRET_KEY'] = 'key'

        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data
    
    def tearDown(self):
        """Remove all traces :) """
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_homepage(self):
        """Test homepage in getting messages"""
        result = self.client.get('/')
        self.assertIn(b"testing", result.data)


if __name__ == '__main__':
    # If called like a script, run our tests
    FlaskTestsBasic()