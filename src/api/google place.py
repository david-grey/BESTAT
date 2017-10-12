# encoding: utf-8

'''

@author: ZiqiLiu


@file: google place.py

@time: 2017/10/8 下午8:45

@desc:
'''
import requests
from googleplaces import GooglePlaces, types, GooglePlacesError
import time


class GooglePlace:
    KEY = 'AIzaSyC394UgcUA4iyyfu-kcm4gOdkKDTM-aFaM'

    PLACE_SEARCH_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    def __init__(self):
        self.sess = requests.session()
        self.googleplace = GooglePlaces(self.KEY)
        pass

    def search_place(self, lat, lon, place_type, radius=1000):
        results = []
        payload = {'location': '{},{}'.format(lat, lon), 'radius': radius,
                   'language': 'en', 'type': place_type, 'key': self.KEY}
        test = set()
        res = requests.get(self.PLACE_SEARCH_URL, params=payload)
        result = res.json()

        while 'next_page_token' in result:
            print(res.url)
            results.extend(result['results'])
            for r in result['results']:
                test.add(r['id'])
            print(result['next_page_token'])

            print(len(test))
            payload['pagetoken'] = result['next_page_token']
            # time.sleep(1)
            res = requests.get(self.PLACE_SEARCH_URL, params=payload)
            result = res.json()
            print(res.url)
        results.extend(result['results'])
        print(len(results))
        return results

    def _nearby_search(self, lat, lon, radius):
        results = []
        query_result = self.googleplace.nearby_search(
            lat_lng={'lat': lat, 'lng': lon}, radius=radius,
            type=types.TYPE_RESTAURANT)
        while query_result.has_next_page_token:
            results.extend([place for place in query_result.places])
            time.sleep(3)
            query_result = self.googleplace.nearby_search(
                lat_lng={'lat': lat, 'lng': lon}, radius=radius,
                type=types.TYPE_RESTAURANT,
                pagetoken=query_result.next_page_token)
        results.extend(query_result.places)
        print(len(results))


googleplace = GooglePlace()
googleplace.search_place(40.4369862, -80.0027261, 'restaurant', 500)
