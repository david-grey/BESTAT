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
import sys

with open('./api/googleplace_chicago.pkl', 'rb') as f:
    data = pickle.load(f)

for key in data:
    records = data[key]
    for id in tqdm(records):
        r = records[id]
        lat = r['lat']
        lng = r['lng']
        nb = get_neighbor(lat, lng)
        if nb:
            setattr(nb.info, key, getattr(nb.info, key) + 1)
            nb.info.save()


