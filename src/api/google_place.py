# encoding: utf-8

'''

@author: ZiqiLiu


@file: google_place.py

@time: 2017/10/8 下午8:45

@desc:
'''
import requests
from .GooglePlaces import GooglePlaces, types, GooglePlacesError
import time
from api.circle import get_circles, default_radius
import pickle
from tqdm import tqdm


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


class GooglePlaceWrap:
    KEY = 'AIzaSyCuCW_ZKBu7U07oEcKz_7hcElbiI02k2VE'
    TYPES = [types.TYPE_HOSPITAL, types.TYPE_RESTAURANT, types.TYPE_STORE,
             types.TYPE_BANK, types.TYPE_SCHOOL, types.TYPE_SUBWAY_STATION,
             types.TYPE_CHURCH, types.TYPE_CAFE, types.TYPE_GYM,
             types.TYPE_GROCERY_OR_SUPERMARKET]

    def __init__(self):
        self.google = GooglePlaces(self.KEY)

    def search_nearby(self, lat, lng, radius):
        places = {}
        for tp in self.TYPES:
            places[tp] = 0
        for key in places:
            count = 0
            result_set = self.google.nearby_search(
                lat_lng={'lat': lat, 'lng': lng},
                radius=radius, type=key)
            count += len(result_set.places)
            while result_set.has_next_page_token:
                try:
                    next_page = self.google.nearby_search(
                        pagetoken=result_set.next_page_token)
                    result_set = next_page
                    count += len(result_set.places)
                except GooglePlacesError:
                    time.sleep(1)
            print(key, count)
            places[key] = count
        return ({'lat': lat, 'lng': lng, 'places': places})

    def search_range(self, points, radius):
        TP = self.TYPES
        places = {}
        for tp in TP:
            places[tp] = {}
        for lat, lng in tqdm(points):
            for key in places:
                sets = []
                result_set = self.google.nearby_search(
                    lat_lng={'lat': lat, 'lng': lng},
                    radius=radius, type=key)
                sets.extend(result_set.places)
                while result_set.has_next_page_token:
                    try:
                        next_page = self.google.nearby_search(
                            pagetoken=result_set.next_page_token)
                        result_set = next_page
                        sets.extend(result_set.places)
                    except GooglePlacesError:
                        time.sleep(1)
                for place in sets:
                    places[key][place.id] = place.geo_location
        return places


if __name__ == '__main__':
    wrapper = GooglePlaceWrap()
    # pittsburgh
    # up = 40.515897
    # down = 40.390015
    # left = -80.046810
    # right = -79.819695
    # chicago
    # up = 42.072
    # down = 41.578
    # left = -88.0
    # right = -87.510

    # new york
    up = 40.9463
    down = 40.4774
    left = -74.2694
    right = -73.6861
    points = get_circles(up, down, left, right)
    print(len(points))

    data = wrapper.search_range(points, default_radius)
    with open('googleplace2.pkl', 'wb') as f:
        pickle.dump(data, f)
