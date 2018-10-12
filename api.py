import os
import requests
import json

YELP = os.environ['YELP_API']
YELP_SEARCH_URL = 'https://api.yelp.com/v3/businesses/search'
YELP_BUSINESS_URL = 'https://api.yelp.com/v3/businesses/'

def get_my_business_details(coordinates):
    """Get business details from YELP API given a list of coordinates"""
    business_list = []
    for coordinate in coordinates:
        latitude = coordinate['lat']
        longitude = coordinate['lng']
        payload = {'latitude': latitude,
                    'longitude': longitude,
                    }
        header = {'Authorization': f"Bearer {YELP}"}
        result = requests.get(YELP_SEARCH_URL, 
                            headers=header,
                             params=payload)
        my_results = json.loads(result.text)
        businesses = my_results['businesses']

        print('\n\n\n\n\n', businesses, '\n\n\n\n\n\n')

        for business in businesses:
            business_id = business['id']
            business_details = requests.get(f"{YELP_BUSINESS_URL} {business_id}",
                                            headers=header)
            if "good-for-kids" in json.loads(business_details.text).attributes:
                business_list.append(business)


    print('\n\n\n\n\n', business_list, '\n\n\n\n\n\n')
    return business_list

def get_playgrounds(coordinates):
    """Get a list of playgrounds from YELP API"""
    playground_list = []
    for coordinate in coordinates:
        latitude = coordinate['lat']
        longitude = coordinate['lng']
        payload = {'latitude': latitude,
                    'longitude': longitude,
                    'categories': 'playgrounds',
                    'radius': 20000
                    }
        header = {'Authorization': f"Bearer {YELP}"}
        result = requests.get(YELP_SEARCH_URL, 
                            headers=header,
                             params=payload)
        my_results = json.loads(result.text)
        playgrounds = my_results['businesses']

        for playground in playgrounds:
            latitude = playground['coordinates']['latitude']
            longitude = playground['coordinates']['longitude']
            name = playground['name']
            playground_list.append({'name': name,
                                    'coords': {'latitude': latitude,
                                                'longitude': longitude}
                                    })

    return playground_list

    