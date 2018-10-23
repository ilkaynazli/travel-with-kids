import os
import requests
import json

YELP = os.environ['YELP_API']
YELP_SEARCH_URL = 'https://api.yelp.com/v3/businesses/search'
YELP_BUSINESS_URL = 'https://api.yelp.com/v3/businesses/'

def get_businesses(coordinates, categories, radius):
    """Get a list of businesses from YELP API"""
    business_list = []
    for coordinate in coordinates:
        latitude = coordinate['lat']
        longitude = coordinate['lng']

        payload = {'latitude': latitude,
                    'longitude': longitude,
                    'categories': categories,
                    'attributes': 'good_for_kids',
                    'radius': radius
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
           
            # aliases = business['categories']
            # for alias in aliases:
            #     for value in alias.values():
            #         if value == 'breakfast_brunch':
            #             business_type = 'br_br'
            #         elif value == 'bbq':
            #             business_type = 'bbq'
            #         elif value == 'burgers':
            #             business_type = 'brgr'
            #         elif value == 'pizza':
            #             business_type = 'pizza'
            #         elif value == 'sandwiches':
            #             business_type = 'sndwc'
            #         elif value == 'icecream':
            #             business_type = 'icecr'
            #         elif value == 'playground':
            #             business_type = 'plygr'
            #         elif value == 'indoor_playcenter':
            #             business_type = 'inply'
            #         elif value == 'carousels':
            #             business_type = 'crsl'
            #         elif value == 'farms':
            #             business_type = 'farm'
            #         elif value == 'zoos':
            #             business_type = 'zoo'
            #         elif value == 'aquariums':
            #             business_type = 'aquar'
            #         else:
            #             business_type = ''

            #     if business_type != '':
            #         break        
            # print('\n\n\n\n', business_type, '\n\n\n\n\n')
            
            business_list.append({'name': name,
                                    'coords': {'latitude': latitude,
                                                'longitude': longitude},
                                    'business_id': business_id,
                                    # 'business_type': business_type
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
