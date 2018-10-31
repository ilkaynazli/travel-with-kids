"""Tests for this project"""

from unittest import TestCase
import unittest

import server
from model import db, example_data, connect_to_db, Business
import json
import functions
import api
from api import YELP_SEARCH_URL, YELP_BUSINESS_URL


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

        def _mock_get_businesses(coordinates, categories, radius):
            """Mock results of get_businesses() function at server.py"""
            business_list = [{'name': 'test',
                                'coords': {'latitude': 32,
                                             'longitude': 120},
                                'business_id': 1,
                                'business_type': 'food'
                                }]
            return business_list

        server.get_businesses = _mock_get_businesses ### Now get_businesses() will return mock data


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

        self.assertIs(json.loads(result.data)['user_id'], None)


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

    def test_show_markers(self):
        """Test the /show-markers.json route"""
        result = self.client.get('/show-markers.json?categories=%22points%3D5000\
                                    %26categories%3Dfood%22&coordinates=%5B%7B\
                                    %22lat%22%3A32%2C%22lng%22%3A120%7D%5D')

        self.assertEqual(json.loads(result.data)[0]['name'], 'test')


    def test_show_maps(self):
        """test the /show-map route"""
        result = self.client.get('/show-map')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<div id="map" data-start=', result.data)
        self.assertIn(b"<script src='/static/js/map.js'></script>", result.data)


    def test_display_signup(self):
        """test display signup page"""

        result = self.client.post('/show-signup-button.json',
                                    content_type='application/json')
        question_id = json.loads(result.data)['questions'][0]['id']
        self.assertEqual(question_id, 1)


    def test_signup(self):
        """test signup page"""
        result = self.client.post('/signup.json',
                                    data=json.dumps({'username':'ilkayn', 
                                                     'password':'123Qwe/',
                                                     'email':'ilkay@ilkay.com',
                                                     'userQuestion': 1,
                                                     'answer':'pink'}),
                                    content_type='application/json')
        
        self.assertEqual(json.loads(result.data)['error'], False)


    def test_user_info_page(self):
        """Test the display user info page"""
        result = self.client.get('/users/1')

        self.assertIn(b'<h1>ilkay</h1>', result.data)


class MyFunctionsUnitTests(TestCase):
    """Test the functions in functions.py"""

    def test_test_the_password(self):
        """Test the password requirements"""
        self.assertEqual(functions.test_the_password('AbCd123*'), False)

    def test_test_the_password_digits(self):
        """Only numbers"""
        self.assertEqual(functions.test_the_password('123456'), True)

    def test_test_the_password_lower(self):
        """Only letters only lower"""
        self.assertEqual(functions.test_the_password('abcdefg'), True)

    def test_test_the_password_upper(self):
        """Only letters no lower"""
        self.assertEqual(functions.test_the_password('ABCDEFG'), True)

    def test_test_the_password_letters(self):
        """Only letters"""
        self.assertEqual(functions.test_the_password('aBcDefg'), True)

    def test_test_the_password_no_chars(self):
        """only letters and digits"""
        self.assertEqual(functions.test_the_password('aBcDefg123'), True)


class ApiCallTestUnitTests(TestCase):
    """Test that mocks yelp api call"""
    def setUp(self):
        """Stuff to do before every test."""

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        server.app.config['SECRET_KEY'] = 'key'

        # Connect to test database (uncomment when testing database)
        connect_to_db(server.app, "testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

        self.old_api = api.yelp_api_call

        def _mock_yelp_api_call(payload_str):
            """Mock results of yelp api call at api.py"""
            return {'businesses':[{'id': 'GLW_lWB5K-4eHX-2RfzJ5g', 
                                'alias': 'davis-poultry-farms-gilroy-10', 
                                'name': 'Davis Poultry Farms', 
                                'image_url': 'https://s3-media1.fl.yelpcdn.com/bphoto/iRY9a_oHXJtLi1W8NDrSbQ/o.jpg', 
                                'is_closed': False, 
                                'url': 'https://www.yelp.com/biz/davis-poultry-farms-gilroy-2?adjust_creative=vxvAyk47rIbZXQHuMg79ww&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=vxvAyk47rIbZXQHuMg79ww', 
                                'review_count': 15, 
                                'categories': [{'alias': 'ranches', 'title': 'Ranches'}], 
                                'rating': 4.5, 
                                'coordinates': {'latitude': 37.0531099, 
                                                'longitude': -121.59012}, 
                                'transactions': [], 
                                'location': {'address1': '155 Santa Clara Ave', 
                                                'address2': '',
                                                'address3': '', 
                                                'city': 'Gilroy', 
                                                'zip_code': '95020', 
                                                'country': 'US', 
                                                'state': 'CA', 
                                                'display_address': ['155 Santa Clara Ave', 'Gilroy, CA 95020']}, 
                                'phone': '+14088424894', 
                                'display_phone': '(408) 842-4894', 
                                'distance': 21479.493719243506}]}            

        api.yelp_api_call = _mock_yelp_api_call


        def _mock_request_get(YELP_SEARCH_URL, headers, params):
            """Mock yelp api request for business search"""
            class MockResult:
                """Mock result of api request"""
                def json(self):
                    return {'businesses':[{'id': 'GLW_lWB5K-4eHX-2RfzJ5g', 
                                        'alias': 'davis-poultry-farms-gilroy-10', 
                                        'name': 'Davis Poultry Farms', 
                                        'image_url': 'https://s3-media1.fl.yelpcdn.com/bphoto/iRY9a_oHXJtLi1W8NDrSbQ/o.jpg', 
                                        'is_closed': False, 
                                        'url': 'https://www.yelp.com/biz/davis-poultry-farms-gilroy-2?adjust_creative=vxvAyk47rIbZXQHuMg79ww&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=vxvAyk47rIbZXQHuMg79ww', 
                                        'review_count': 15, 
                                        'categories': [{'alias': 'ranches', 'title': 'Ranches'}], 
                                        'rating': 4.5, 
                                        'coordinates': {'latitude': 37.0531099, 
                                                        'longitude': -121.59012}, 
                                        'transactions': [], 
                                        'location': {'address1': '155 Santa Clara Ave', 
                                                        'address2': '',
                                                        'address3': '', 
                                                        'city': 'Gilroy', 
                                                        'zip_code': '95020', 
                                                        'country': 'US', 
                                                        'state': 'CA', 
                                                        'display_address': ['155 Santa Clara Ave', 'Gilroy, CA 95020']}, 
                                        'phone': '+14088424894', 
                                        'display_phone': '(408) 842-4894', 
                                        'distance': 21479.493719243506}]}
            my_result = MockResult()
            return my_result

        api.requests.get = _mock_request_get


    def test_yelp_api_call(self):
        """Test the yelp api call function"""
        coordinate = {'lat': 37.2595209380423, 
                      'lng': -121.831776984036}
        categories = 'markets, playgrounds, icecream, ranches'
        radius = 12500
        url = YELP_SEARCH_URL
        payload = {'latitude': coordinate['lat'],
                    'longitude': coordinate['lng'],
                    'categories': categories,
                    'attributes': 'good_for_kids',
                    'radius': radius
                    }
        # import pdb; pdb.set_trace()
        test_result = api.yelp_api_call(payload)
        self.assertEqual(test_result['businesses'][0]['name'],'Davis Poultry Farms')

   
    def test_find_the_category_of_business(self):
        """test if the returned value is correct"""
        categories = [{'alias':'parks'},
                      {'alias': 'churches'},
                      {'alias': 'playgrounds'},
                      {'alias': 'zoos'},
                      {'alias': 'ranches'}]
        self.assertEqual(api.find_the_category_of_business(categories), 'plygr')

   
    def test_find_the_category_of_business_not_there(self):
        """test if the returned value is correct"""
        categories = [{'alias':'daycares'},
                      {'alias': 'schools'}]
        self.assertEqual(api.find_the_category_of_business(categories), '')


    def test_add_business_info_to_list(self):
        """Test if the function can successfully add a business dictionary to a list"""

        businesses = [ {'id': 'BgKmy9wX5GH6w-Llk5LW_Q', 
                        'alias': 'jacobs-farms-san-jose-2', 
                        'name': 'Jacobs Farms', 
                        'image_url': 'https://s3-media3.fl.yelpcdn.com/bphoto/AqEVq-1C42yPDhTJe0RD7A/o.jpg', 
                        'is_closed': False, 
                        'url': 'https://www.yelp.com/biz/jacobs-farms-san-jose-2?adjust_creative=vxvAyk47rIbZXQHuMg79ww&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=vxvAyk47rIbZXQHuMg79ww', 
                        'review_count': 19, 
                        'categories': [{'alias': 'pumpkinpatches', 'title': 'Pumpkin Patches'}, 
                                        {'alias': 'markets', 'title': 'Fruits & Veggies'}, 
                                        {'alias': 'pickyourown', 'title': 'Pick Your Own Farms'}], 
                        'rating': 4.5, 
                        'coordinates': {'latitude': 37.2595209380423, 
                                        'longitude': -121.831776984036}, 
                        'transactions': [], 
                        'price': '$$', 
                        'location': {'address1': '5285 Snell Ave', 
                                        'address2': '', 
                                        'address3': '', 
                                        'city': 'San Jose', 
                                        'zip_code': '95136', 
                                        'country': 'US', 
                                        'state': 'CA', 
                                        'display_address': ['5285 Snell Ave', 'San Jose, CA 95136']}, 
                        'phone': '+14083359136', 
                        'display_phone': '(408) 335-9136', 
                        'distance': 10673.690101679851}, 
                       {'id': 'GLW_lWB5K-4eHX-2RfzJ5g', 
                        'alias': 'davis-poultry-farms-gilroy-2', 
                        'name': 'Davis Poultry Farms', 
                        'image_url': 'https://s3-media1.fl.yelpcdn.com/bphoto/iRY9a_oHXJtLi1W8NDrSbQ/o.jpg', 
                        'is_closed': False, 
                        'url': 'https://www.yelp.com/biz/davis-poultry-farms-gilroy-2?adjust_creative=vxvAyk47rIbZXQHuMg79ww&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=vxvAyk47rIbZXQHuMg79ww', 
                        'review_count': 15, 
                        'categories': [{'alias': 'ranches', 'title': 'Ranches'}], 
                        'rating': 4.5, 
                        'coordinates': {'latitude': 37.0531099, 
                                        'longitude': -121.59012}, 
                        'transactions': [], 
                        'location': {'address1': '155 Santa Clara Ave', 
                                        'address2': '',
                                        'address3': '', 
                                        'city': 'Gilroy', 
                                        'zip_code': '95020', 
                                        'country': 'US', 
                                        'state': 'CA', 
                                        'display_address': ['155 Santa Clara Ave', 'Gilroy, CA 95020']}, 
                        'phone': '+14088424894', 
                        'display_phone': '(408) 842-4894', 
                        'distance': 21479.493719243506}, 
                       {'id': 'NdLOM_QH6POZ9cd2IH6LTA', 
                        'alias': 'bernal-gulnac-joice-ranch-san-jose', 
                        'name': 'Bernal Gulnac Joice Ranch', 
                        'image_url': 'https://s3-media4.fl.yelpcdn.com/bphoto/2z-J9VXWmbx29lmcrDB7oQ/o.jpg', 
                        'is_closed': False, 
                        'url': 'https://www.yelp.com/biz/bernal-gulnac-joice-ranch-san-jose?adjust_creative=vxvAyk47rIbZXQHuMg79ww&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=vxvAyk47rIbZXQHuMg79ww', 
                        'review_count': 2, 
                        'categories': [{'alias': 'ranches', 'title': 'Ranches'}], 
                        'rating': 4.5, 
                        'coordinates': {'latitude': 37.2263304364867, 
                                        'longitude': -121.798300668597}, 
                        'transactions': [], 
                        'location': {'address1': '372 Manila Dr', 
                                     'address2': '', 
                                     'address3': '', 
                                     'city': 'San Jose', 
                                     'zip_code': '95119', 
                                     'country': 'US', 
                                     'state': 'CA', 
                                     'display_address': ['372 Manila Dr', 'San Jose, CA 95119']}, 
                        'phone': '+14082265453', 
                        'display_phone': '(408) 226-5453',
                        'distance': 6537.030263122577}]
        business_list = []
        api.add_business_info_to_list(business_list, businesses)
        self.assertEqual(business_list[2]['business_id'], 'NdLOM_QH6POZ9cd2IH6LTA')

    def test_add_business_info_to_list_wrong(self):
        """Test if the function can successfully add a business dictionary to a list"""

        businesses = [ {'id': 'BgKmy9wX5GH6w-Llk5LW_Q', 
                        'alias': 'jacobs-farms-san-jose-2', 
                        'name': 'Jacobs Farms', 
                        'image_url': 'https://s3-media3.fl.yelpcdn.com/bphoto/AqEVq-1C42yPDhTJe0RD7A/o.jpg', 
                        'is_closed': False, 
                        'url': 'https://www.yelp.com/biz/jacobs-farms-san-jose-2?adjust_creative=vxvAyk47rIbZXQHuMg79ww&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=vxvAyk47rIbZXQHuMg79ww', 
                        'review_count': 19, 
                        'categories': [{'alias': 'pumpkinpatches', 'title': 'Pumpkin Patches'}, 
                                        {'alias': 'markets', 'title': 'Fruits & Veggies'}, 
                                        {'alias': 'pickyourown', 'title': 'Pick Your Own Farms'}], 
                        'rating': 4.5, 
                        'coordinates': {'latitude': 37.2595209380423, 
                                        'longitude': -121.831776984036}, 
                        'transactions': [], 
                        'price': '$$', 
                        'location': {'address1': '5285 Snell Ave', 
                                        'address2': '', 
                                        'address3': '', 
                                        'city': 'San Jose', 
                                        'zip_code': '95136', 
                                        'country': 'US', 
                                        'state': 'CA', 
                                        'display_address': ['5285 Snell Ave', 'San Jose, CA 95136']}, 
                        'phone': '+14083359136', 
                        'display_phone': '(408) 335-9136', 
                        'distance': 10673.690101679851}]
        business_list = []
        api.add_business_info_to_list(business_list, businesses)
        self.assertNotEqual(business_list[0]['name'], 'Davis Poultry Farms')

    
    def test_get_businesses(self):
        """Test get businesses from yelp api"""
        coordinates = [{'lat': 37.2595209380423, 
                        'lng': -121.831776984036}]
        categories = 'markets, playgrounds, icecream'
        radius = 12500
        my_result = api.get_businesses(coordinates, categories, radius)[0]['name']
        self.assertEqual(my_result, 'Davis Poultry Farms')


    def tearDown(self):
        """Do at end of every test."""
        api.yelp_api_call = self.old_api

        db.session.close()
        db.drop_all()


class ApiCallSecondTestUnitTests(TestCase):
    """Test that mocks yelp api call"""
    def setUp(self):
        """Stuff to do before every test."""

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        server.app.config['SECRET_KEY'] = 'key'

        def _mock_request_get2(YELP_BUSINESS_URL, headers, params):
            """Mock yelp api request for business search"""
            class MockResult:
                """Mock result of api request"""
                def json(self):
                    return {'id': '9tR_vXF3ugf6zvcRVqf0VA', 
                              'alias': 'mooyah-burger-fries-and-shakes-morgan-hill-5', 
                              'name': 'Mooyah Burger Fries & Shakes', 
                              'image_url': 'https://s3-media1.fl.yelpcdn.com/bphoto/DDdDDKARApoNg2fJo6yxYg/o.jpg', 
                              'is_claimed': True, 
                              'is_closed': False, 
                              'url': 'https://www.yelp.com/biz/mooyah-burger-fries-and-shakes-morgan-hill-5?adjust_creative=vxvAyk47rIbZXQHuMg79ww&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_lookup&utm_source=vxvAyk47rIbZXQHuMg79ww', 
                              'phone': '+14087792255', 
                              'display_phone': '(408) 779-2255', 
                              'review_count': 258, 
                              'categories': [
                                        {'alias': 'burgers', 'title': 'Burgers'}, 
                                        {'alias': 'icecream', 'title': 'Ice Cream & Frozen Yogurt'}, 
                                        {'alias': 'hotdogs', 'title': 'Fast Food'}], 
                               'rating': 3.5, 
                               'location': {'address1': '255 Vineyard Town Ctr', 
                                            'address2': '', 
                                            'address3': '', 
                                            'city': 'Morgan Hill', 
                                            'zip_code': '95037', 
                                            'country': 'US', 
                                            'state': 'CA', 
                                            'display_address': ['255 Vineyard Town Ctr', 'Morgan Hill, CA 95037'], 
                                            'cross_streets': ''}, 
                               'coordinates': {'latitude': 37.1121749699774, 
                                               'longitude': -121.643401704356}, 
                               'photos': ['https://s3-media1.fl.yelpcdn.com/bphoto/DDdDDKARApoNg2fJo6yxYg/o.jpg', 
                                          'https://s3-media4.fl.yelpcdn.com/bphoto/jLvyfQR_S6WQztoxDKqKTA/o.jpg', 
                                          'https://s3-media2.fl.yelpcdn.com/bphoto/ezG4-V8whbnhGYWXAQ1pYg/o.jpg'], 
                               'price': '$$', 
                               'hours': [{'open': 
                                            [{'is_overnight': False, 'start': '1100', 'end': '2100', 'day': 0}, 
                                             {'is_overnight': False, 'start': '1100', 'end': '2100', 'day': 1}, 
                                             {'is_overnight': False, 'start': '1100', 'end': '2100', 'day': 2}, 
                                             {'is_overnight': False, 'start': '1100', 'end': '2100', 'day': 3}, 
                                             {'is_overnight': False, 'start': '1100', 'end': '2200', 'day': 4}, 
                                             {'is_overnight': False, 'start': '1100', 'end': '2200', 'day': 5}, 
                                             {'is_overnight': False, 'start': '1100', 'end': '2100', 'day': 6}], 
                                          'hours_type': 'REGULAR', 
                                          'is_open_now': True}], 
                               'transactions': []}
 
            my_result = MockResult()
            return my_result

        api.requests.get = _mock_request_get2

    def test_business_info_page(self):
        """Test the display business info page"""
        result = self.client.get('/business/9tR_vXF3ugf6zvcRVqf0VA')

        self.assertIn(b"<h1>Welcome to the Mooyah Burger Fries &amp; Shakes page</h1>", result.data)


    def test_get_business_info(self):
        """Test the yelp api call function"""
        business_id = '9tR_vXF3ugf6zvcRVqf0VA'
 
        test_result = api.get_business_info(business_id)
        self.assertEqual(test_result['name'],'Mooyah Burger Fries & Shakes')


if __name__ == "__main__":
    unittest.main()





