# encoding: utf-8

'''

@author: ZiqiLiu


@file: googleplace_scrapy.py

@time: 2017/11/13 下午8:49

@desc:
'''

import pickle
from api.google_place import GooglePlaceWrap
from api.circle import get_circles, default_radius
from api.GooglePlaces import GooglePlacesError
import sys

Quota = 150000

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

    with open('./bestat/data/remain_city.pkl', 'rb') as f:
        cities = pickle.load(f)
    keys = list(cities.keys())
    for k in keys:
        try:
            bound = cities[k]
            points = get_circles(bound[0], bound[1], bound[2], bound[3])
            print('city %s, %d points' % (k, len(points)))
            if len(points) >= 30000:
                continue
            if len(points) * 13 >= Quota:
                print('today finished. %d cities remaining' % len(cities))
                with open('./bestat/data/remain_city.pkl', 'wb') as f:
                    pickle.dump(cities, f)
                break
            else:
                data, quota = wrapper.search_range(points, default_radius)
                Quota -= quota
                with open('./bestat/data/googleplace_%s.pkl' % (
                        '+'.join(k.split()).strip()),
                          'wb') as f:
                    pickle.dump(data, f)
                del cities[k]
                print('city %s finished, remaining quota %d' % (k, Quota))
                with open('./bestat/data/remain_city.pkl', 'wb') as f:
                    pickle.dump(cities, f)
        except GooglePlacesError as e:
            print(e)
            with open('./bestat/data/remain_city.pkl', 'wb') as f:
                print('today finished. %d cities remaining' % len(cities))
                pickle.dump(cities, f)
            sys.exit(1)
