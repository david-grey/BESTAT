# encoding: utf-8

'''

@author: ZiqiLiu


@file: load_data.py

@time: 2017/11/4 下午2:40

@desc:
'''

from bestat.utils import get_neighbor
import pickle

with open('./api/googleplace_pitts.pkl', 'rb') as f:
    data = pickle.load(f)

for key in data:
    records = data[key]
    for id in records:
        r = records[id]
        lat = r['lat']
        lng = r['lng']
        nb = get_neighbor(lat, lng)
        nb.info.objects.update()

