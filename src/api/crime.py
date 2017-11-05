# encoding: utf-8

'''

@author: ZiqiLiu


@file: crime.py

@time: 2017/10/8 下午2:59

@desc:
'''

# https://spotcrime.com/pa/pittsburgh/daily-blotter/2017-10-07
# https://spotcrime.com/pa/pittsburgh/neighborhoods
# https://spotcrime.com/pa/pittsburgh/allegheny+center

import requests
import pickle
from api.circle import get_circles
from tqdm import tqdm

BASE_URL = 'https://spotcrime.com'

CRIME_SCORE = {'Theft': 2, 'Robbery': 3, 'Burglary': 3,
               'Vandalism': 2, 'Shooting': 5, 'Arson': 4, 'Arrest': 4,
               'Assault': 4, 'Other': 1}

RADIUS = 0.005


# incidents type: Theft, Robbery, Burglary, Vandalism, Shooting,
#                  Arson, Arrest, Assault, Other


class Crime:
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    _url = 'https://api.spotcrime.com/crimes.json?lat={}&lon={}&radius={}&key={}'
    _key = 'privatekeyforspotcrimepublicusers-commercialuse-877.410.1607'

    def _fetch(self, lat, lng, radius):
        res = requests.get(
            self._url.format(lat, lng, radius, self._key),
            headers=self.header).json()
        return res['crimes'] if 'crimes' in res else []

    def fetch_range(self, points):
        data = {}
        for tp in CRIME_SCORE:
            data[tp] = {}
        for lat, lng in tqdm(points):
            res = self._fetch(lat, lng, RADIUS)
            for r in res:
                data[r['type']][r['cdid']] = r
        return data


if __name__ == '__main__':
    crime = Crime()
    # pittsburgh
    # up = 40.515897
    # down = 40.390015
    # left = -80.046810
    # right = -79.819695

    # # chicago
    # up = 42.072
    # down = 41.578
    # left = -88.0
    # right = -87.510

    # new york
    up = 40.9463
    down = 40.4774
    left = -74.2694
    right = -73.6861

    data = crime.fetch_range(get_circles(up, down, left, right, RADIUS))
    with open('crime_newyork.pkl', 'wb') as f:
        pickle.dump(data, f)


    # print(crime._fetch(41.788,-87.765,0.006))
