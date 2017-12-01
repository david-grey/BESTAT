# encoding: utf-8

'''

@author: ZiqiLiu


@file: load_googledata.py

@time: 2017/11/4 下午2:40

@desc:
'''

from bestat.utils import get_neighbor, clean_crime
from bestat.models import Neighbor
import pickle
from tqdm import tqdm
from glob import glob


def load_crime(fi):
    city = ' '.join(fi.split('_')[-1].split('.')[0].split('+'))
    clean_crime(city)
    print('loading crime data of city %s...' % city)
    with open(fi, 'rb') as f:
        data = pickle.load(f)

    for key in data:
        records = data[key]
        for id in tqdm(records):
            r = records[id]
            lat = r['lat']
            lng = r['lon']
            nb = get_neighbor(lat, lng)
            if nb and nb.city == city:
                setattr(nb.crimes, key, getattr(nb.crimes, key) + 1)
                nb.crimes.save()


def batch_load():
    files = glob('./bestat/data/crime/crime_*.pkl')
    for fi in tqdm(files):
        load_crime(fi)


if __name__ == '__main__':
    batch_load()
