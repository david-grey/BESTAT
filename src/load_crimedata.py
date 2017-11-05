# encoding: utf-8

'''

@author: ZiqiLiu


@file: load_googledata.py

@time: 2017/11/4 下午2:40

@desc:
'''

from bestat.utils import get_neighbor
import pickle
from tqdm import tqdm

with open('./api/crime_pitts.pkl', 'rb') as f:
    data = pickle.load(f)

for key in data:
    records = data[key]
    for id in tqdm(records):
        r = records[id]
        lat = r['lat']
        lng = r['lon']
        nb = get_neighbor(lat, lng)
        if nb:
            setattr(nb.crimes, key, getattr(nb.crimes, key) + 1)
            nb.crimes.save()
