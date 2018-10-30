import os
import requests
import json
from model import Business, db


YELP = os.environ['YELP_API']
YELP_SEARCH_URL = 'https://api.yelp.com/v3/businesses/search'
YELP_BUSINESS_URL = 'https://api.yelp.com/v3/businesses/'
BUSINESS_TYPES = {
                    'breakfast_brunch': 'br_br',
                    'bbq':'bbq',
                    'burgers': 'brgr',
                    'pizza': 'pizza',
                    'sandwiches': 'sndwc',
                    'icecream': 'icecr',
                    'playgrounds': 'plygr',
                    'indoor_playcenter': 'inply',
                    'carousels': 'crsl',
                    'farms': 'farm',
                    'zoos': 'zoo',
                    'aquariums': 'aquar'
                    }


def get_businesses(coordinates, categories, radius):
    """Get a list of businesses from YELP API"""
    business_list = []
    
    for coordinate in coordinates: 

        my_results = yelp_api_call(coordinate, categories, radius)
        add_business_info_to_list(business_list, my_results['businesses'])
                                
    return business_list


def yelp_api_call(coordinate, categories, radius):
    """Yelp API call for a single coordinate data from google maps"""
    latitude = coordinate['lat']
    longitude = coordinate['lng']
    payload = {'latitude': latitude,
                'longitude': longitude,
                'categories': categories,
                'attributes': 'good_for_kids',
                'radius': radius
                }
    header = {'Authorization': f"Bearer {YELP}"}
    result = requests.get(YELP_SEARCH_URL, headers=header, params=payload)
    return result.json()


def get_business_info(business_id):
    """Get info on business given its YELP id"""

    header = {'Authorization': f"Bearer {YELP}"}
    business = requests.get(f"{YELP_BUSINESS_URL}{business_id}",
                                        headers=header,
                                        params=None)
    business = business.json()

    business_info = {
        "name": business['name'],
        "formatted_phone_number": business['display_phone'],
        "yelp_url": business['url'],
        "photo": business['photos'],
        "formatted_address": " ".join(business['location']['display_address']),
        "location":{'lat':business['coordinates']['latitude'],
                    'lng':business['coordinates']['longitude']}
    } 
    return business_info


def add_business_info_to_list(business_list, businesses):
    """List of coordinates, name, business id and type dictionaries"""

    for business in businesses:
        latitude = business['coordinates']['latitude']
        longitude = business['coordinates']['longitude']
        name = business['name']
        business_id = business['id']
        categories_list = business['categories']
        business_type = find_the_category_of_business(categories_list)
        my_business = {'name': name,
                        'coords': {'latitude': latitude,
                                    'longitude': longitude},
                        'business_id': business_id,
                        'business_type': business_type
                        }

        if Business.query.filter(Business.business_id == my_business.get('business_id')).first() == None:
            add_business_to_database(business_id, name, business_type, latitude, longitude)

        business_list.append(my_business)


def find_the_category_of_business(categories):
    """Find the category of the business and return its type"""

    for category in categories:
        alias = category['alias']
        if alias in BUSINESS_TYPES:
            business_type = BUSINESS_TYPES[alias]
            break
        else:
            business_type = ''
    return business_type

def add_business_to_database(business_id, name, business_type, latitude, longitude):
    """Add business to the database"""
    business = Business(business_id=business_id,
                                business_name=name,
                                business_type=business_type,
                                latitude=latitude,
                                longitude=longitude)
    db.session.add(business)
    db.session.commit()  
