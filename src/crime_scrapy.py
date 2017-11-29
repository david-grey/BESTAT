# encoding: utf-8

'''

@author: ZiqiLiu


@file: googleplace_scrapy.py

@time: 2017/11/13 下午8:49

@desc:
'''

import pickle
from api.crime import Crime, RADIUS
from api.circle import get_circles
import traceback
import sys
import json
import time

if __name__ == '__main__':
    wrapper = Crime()

    with open('./bestat/data/crime_remain_city.pkl', 'rb') as f:
        cities = pickle.load(f)

    keys = list(cities.keys())

    keys = ['New York', 'Chicago']
    for k in keys:
        try:
            bound = cities[k]
            points = get_circles(bound[0], bound[1], bound[2], bound[3], RADIUS)
            if len(points) >= 30000:
                print('skip city %s, %d points' % (k, len(points)))
                continue
            print('city %s, %d points' % (k, len(points)))

            data = wrapper.fetch_range(points)
            with open('./bestat/data/crime/crime_%s.pkl' % (
                    '+'.join(k.split()).strip()),
                      'wb') as f:
                pickle.dump(data, f)
            del cities[k]
            with open('./bestat/data/crime_remain_city.pkl', 'wb') as f:
                pickle.dump(cities, f)
            print('city %s finished' % (k))
        except json.decoder.JSONDecodeError as e:
            print('banned, sleep for 5 minutes')
            time.sleep(300)
        except Exception or KeyboardInterrupt as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(e)
            print(traceback.print_exception(exc_type, exc_value, exc_traceback,
                                            limit=2, file=sys.stdout))
            with open('./bestat/data/crime_remain_city.pkl', 'wb') as f:
                print('today finished. %d cities remaining' % len(cities))
                pickle.dump(cities, f)
            sys.exit(1)
