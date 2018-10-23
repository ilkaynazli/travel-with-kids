"""Tests for this project"""

from unittest import TestCase
import unittest

import server
from model import db, example_data, connect_to_db
import json

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(server.app, "testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_homepage(self):          #have to change this later
        """Test homepage"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<form action="/show-map"', result.data)


    def test_login(self):
        """Test login page."""
        result = self.client.post("/login.json",
                                    data=json.dumps({'username': "ilkay", 
                                                        'password': "123Qwe/"}),
                                content_type='application/json')

        self.assertEqual(result.status_code, 200)                       
        self.assertIs(json.loads(result.data)['user_id'], 1)

    # def test_login_wrong_username(self):
    #     """test wrong password or username"""

    #     result = self.client.post("/login",
    #                               data={"user_id": "ilkayn", 
    #                                     "password": "123QWe/"},
    #                               follow_redirects=True)
    #     self.assertIn(b"Username does not exist. Please sign up.", result.data)


    # def test_login_wrong_password(self):
    #     """test wrong password or username"""

    #     result = self.client.post("/login",
    #                               data={"user_id": "ilkay", 
    #                                     "password": "123qwE/"},
    #                               follow_redirects=True)
    #     self.assertIn(b"Username does not exist. Please sign up.", result.data)
    # def test_wrong_password(self):
    #     """Wrong password page"""

    #     result = self.client.get("/wrong-password")
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"Please enter your email:", result.data)

    # def test_forgot_password(self):
    #     """check answers"""
        
    #     pass

    # def test_signup(self):
    #     """test signup page"""

    #     pass


if __name__ == "__main__":
    unittest.main()