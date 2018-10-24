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
        server.app.config['SECRET_KEY'] = 'key'

        with self.client as c:
            with c.session_transaction() as sess:
                sess['email'] = 'ilkay@ilkay.com'
                sess['user_id'] = 1

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


    def test_login_wrong_username(self):
        """test wrong password or username"""
        result = self.client.post("/login.json",
                                  data=json.dumps({"user_id": "ilkayn", 
                                        "password": "123QWe/"}),
                                  content_type='application/json')

        self.assertIs(json.loads(result.data)['error'], True)


    def test_login_wrong_password(self):
        """test wrong password or username"""
        result = self.client.post("/login.json",
                                  data=json.dumps({"user_id": "ilkay", 
                                        "password": "123qwE/"}),
                                  content_type='application/json')

        self.assertIs(json.loads(result.data)['error'], True)


    def test_forgot_password(self):
        """Forgot password page, take email address of user"""

        result = self.client.post("/forgot-password.json",
                                    data=json.dumps({'email': 'ilkay@ilkay.com'}),
                                    content_type='application/json')

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data)['question'], 'Favorite color?')

    def test_forgot_password_wrong_email(self):
        """Forgot password page, take email address of user"""

        result = self.client.post("/forgot-password.json",
                                    data=json.dumps({'email': 'ilkayn@ilkay.com'}),
                                    content_type='application/json')

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data)['question'], None)   


    def test_check_answer(self):
        """Check if the answer is correct"""
        result = self.client.post('check-answer.json',
                                    data=json.dumps({'answer': 'blue'}),
                                    content_type='application/json')

        self.assertEqual(json.loads(result.data)['error'], False)
        self.assertEqual(json.loads(result.data)['username'], 'ilkay')

    def test_check_answer_wrong_answer(self):
        """Check if the answer is correct"""
        result = self.client.post('check-answer.json',
                                    data=json.dumps({'answer': 'pink'}),
                                    content_type='application/json')

        self.assertEqual(json.loads(result.data)['error'], True)
        self.assertEqual(json.loads(result.data)['username'], '')


    def test_new_password(self):
        """Test if the new password page is working"""
        result = self.client.post('/new-password.json',
                                    data=json.dumps({'password': '321eWQ/'}),
                                    content_type='application/json')

        self.assertEqual(json.loads(result.data)['error'], False)


    def test_new_password_not_correct(self):
        """Test if the new password page is working"""
        result = self.client.post('/new-password.json',
                                    data=json.dumps({'password': '321eWQ'}),
                                    content_type='application/json')

        self.assertEqual(json.loads(result.data)['error'], True)

    def test_logout(self):
        """Test logout route"""
        result = self.client.get('/log-out',
                                follow_redirects=True)

        self.assertIn(b'<form action="/show-map"', result.data)
        # self.assertNotEqual(sess['user_id'], 1)                   ### How can I test if a session is removed?



    # def test_signup(self):
    #     """test signup page"""

    #     pass


if __name__ == "__main__":
    unittest.main()