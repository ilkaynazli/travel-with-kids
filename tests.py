"""Tests for this project"""

import unittest

from server import app
from model import db, example_data, connect_to_db

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