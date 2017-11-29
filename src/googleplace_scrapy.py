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
from load_googledata import load_data

Quota = 150000


def scrap():
    global Quota
    wrapper = GooglePlaceWrap()
    with open('./bestat/data/googleplace/remain_city.pkl', 'rb') as f:
        cities = pickle.load(f)
    keys = list(cities.keys())
    for city in keys:
        try:
            bound = cities[city]
            points = get_circles(bound[0], bound[1], bound[2], bound[3])
            print('city %s, %d points' % (city, len(points)))
            if len(points) >= 30000:
                continue
            # if len(points) * 13 >= Quota:
            #     print('today finished. %d cities remaining' % len(cities))
            #     with open('./bestat/data/googleplace/remain_city.pkl',
            #               'wb') as f:
            #         pickle.dump(cities, f)
            #     break

            data, quota = wrapper.search_range(points, default_radius)
            Quota -= quota
            pkl_name = 'googleplace_%s.pkl' % '+'.join(city.split()).strip()
            with open('./bestat/data/googleplace/%s' % pkl_name, 'wb') as f:
                pickle.dump(data, f)

            load_data(pkl_name)

            del cities[city]
            print('city %s finished, remaining quota %d' % (city, Quota))
            with open('./bestat/data/googleplace/remain_city.pkl',
                      'wb') as f:
                pickle.dump(cities, f)
        except GooglePlacesError as e:
            print(e)
            with open('./bestat/data/googleplace/remain_city.pkl', 'wb') as f:
                print('today finished. %d cities remaining' % len(cities))
                pickle.dump(cities, f)
            sys.exit(1)


if __name__ == '__main__':
    scrap()
