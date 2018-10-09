"""Tests for this project"""

import unittest

from server import app
from model import db, example_data, connect_to_db

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):          #have to change this later
        """Test homepage"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Hello there!</h1>', result.data)

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"user_id": "ilkayn", 
                                        "password": "123QWe/"},
                                  follow_redirects=True)
        self.assertIn(b"You have logged in.", result.data)

    def test_login_wrong(self):
        """test wrong password or username"""

        result = self.client.post("/login",
                                  data={"user_id": "ilkay", 
                                        "password": "123QWe/"},
                                  follow_redirects=True)
        self.assertIn(b"Wrong username or password.", result.data)

    def test_signup(self):
        """test signup page"""

        pass

    def test_forgot_password(self):
        """Forgot password page"""

        result = self.client.get("/wrong-password")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Please enter your email:", result.data)

    def test_forgot_password(self):
        """check answers"""

        pass


class TravelTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        
        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()




if __name__ == "__main__":
    unittest.main()