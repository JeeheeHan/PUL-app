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




if __name__ == '__main__':
    # If called like a script, run our tests
    FlaskTestsBasic()