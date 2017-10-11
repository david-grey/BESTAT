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
from bs4 import BeautifulSoup
import re
from dateutil.parser import parser
from datetime import datetime
import time

BASE_URL = 'https://spotcrime.com'

DATA_DICT = {'Theft': None, 'Robbery': None, 'Burglary': None,
             'Vandalism': None, 'Shooting': None, 'Arson': None, 'Arrest': None,
             'Assault': None, 'Other': None}

CRIME_SCORE = {'Theft': 2, 'Robbery': 3, 'Burglary': 3,
               'Vandalism': 2, 'Shooting': 5, 'Arson': 4, 'Arrest': 4,
               'Assault': 4, 'Other': 1}


# incidents type: Theft, Robbery, Burglary, Vandalism, Shooting,
#                  Arson, Arrest, Assault, Other


class Neighborhood:
    BASE_URL = 'https://spotcrime.com'

    def __init__(self, name='Garfield',
                 url='/pa/pittsburgh/garfield'):
        self.name = name
        self._url = url
        page = requests.get(self.url).content
        soup = BeautifulSoup(page, 'html5lib')
        trs = soup.find('div', class_='text-left').find_all('div',
                                                            class_='panel panel-default')[
            -1].find('tbody').find_all('tr')

        self.data = dict(DATA_DICT)

        for tr in trs:
            # incidents,  last week,  last 30days,  previous 30days, last six month

            self.data[tr.th.text] = int(tr.find_all('td')[-1].text)

        print(self.name, self.data)

    @property
    def url(self):
        return self.BASE_URL + self._url

    def __str__(self):
        return self.data


class City:
    BASE_URL = 'https://spotcrime.com'

    def __init__(self, state='pa', city='pittsburgh'):
        self.state = state.lower()
        self.city = city.lower()
        page = requests.get(
            'https://spotcrime.com/%s/%s/neighborhoods' % (
                self.state, self.city)).content
        soup = BeautifulSoup(page, 'html5lib')

        table = soup.find(name='table',
                          class_='table table-condensed table-striped table-hover text-left').tbody
        print('fuck')
        neighbors = table.find_all(name='td')
        self.neighbors = []
        for neighbor in neighbors:
            time.sleep(2)
            name = \
                neighbor.find('googlePlaceType.txt').text.split(' Crime Map')[0]
            url = neighbor.find('googlePlaceType.txt')['href']
            self.neighbors.append(Neighborhood(name, url))

    def print(self):
        for nei in self.neighbors:
            print(nei.name)
            print(nei)


def test(lat, lon, radius=0.01):
    url = 'https://api.spotcrime.com/crimes.json?lat={}&lon={}&radius={}&key=privatekeyforspotcrimepublicusers-commercialuse-877.410.1607&_=1507525220192'.format(
        lat, lon, radius)
    print(requests.get(url))


class Crime:
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    _url = 'https://api.spotcrime.com/crimes.json?lat={}&lon={}&radius={}&key={}'
    _key = 'privatekeyforspotcrimepublicusers-commercialuse-877.410.1607'

    def fetch(self, lat, lon, radius=0.006):
        res = requests.get(
            self._url.format(lat, lon, radius, self._key),
            headers=self.header).json()
        return res['crimes'] if 'crimes' in res else None

    def crime_index(self, lat, lon, radius=0.06):
        records = self.fetch(lat, lon, radius)
        if len(records) == 0:
            return 0
        t1 = datetime.strptime(li[0]['date'], '%m/%d/%y %I:%M %p')
        t2 = datetime.strptime(li[-1]['date'], '%m/%d/%y %I:%M %p')
        scores = sum([CRIME_SCORE[record['type']] for record in records])

        return scores / (t1 - t2).days


if __name__ == '__main__':
    # test(40.4523945, -79.92007064)
    crime = Crime()
    li = crime.fetch(40.4463508, -79.9804448)
    score = crime.crime_index(40.4463508, -79.9804448)
    print(score)

# city = City()
# city.print()
# nb = Neighborhood()
