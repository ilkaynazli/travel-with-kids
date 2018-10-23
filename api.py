import os
import requests
import json

YELP = os.environ['YELP_API']
YELP_SEARCH_URL = 'https://api.yelp.com/v3/businesses/search'
YELP_BUSINESS_URL = 'https://api.yelp.com/v3/businesses/'

def get_businesses(coordinates, categories):
    """Get a list of businesses from YELP API"""
    business_list = []
    for coordinate in coordinates:
        latitude = coordinate['lat']
        longitude = coordinate['lng']

        payload = {'latitude': latitude,
                    'longitude': longitude,
                    'categories': categories,
                    'attributes': 'good_for_kids',
                    'radius': 20000
                    }
        header = {'Authorization': f"Bearer {YELP}"}
        result = requests.get(YELP_SEARCH_URL, 
                            headers=header,
                             params=payload)
        my_results = result.json()
        businesses = my_results['businesses']

        for business in businesses:
            latitude = business['coordinates']['latitude']
            longitude = business['coordinates']['longitude']
            name = business['name']
            business_id = business['id']
            business_list.append({'name': name,
                                    'coords': {'latitude': latitude,
                                                'longitude': longitude},
                                    'business_id': business_id,
                                    })

    return business_list


def get_business_info(business_id):
    """Get info on business given its YELP id"""

    header = {'Authorization': f"Bearer {YELP}"}

    business = requests.get(f"{YELP_BUSINESS_URL}{business_id}",
                                        headers=header)

    business = business.json()

    business_info = {
        'name': business['name'],
        'phone': business['phone'],
        'url': business['url'],
        'photos': business['photos'],
        'address': " ".join(business['location']['display_address'])
    } 

    return business_info
