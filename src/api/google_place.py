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

Quota = 150000


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
    # up = 40.9463
    # down = 40.4774
    # left = -74.2694
    # right = -73.6861
    # points = get_circles(up, down, left, right)

