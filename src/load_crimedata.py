# encoding: utf-8

'''

@author: ZiqiLiu


@file: load_googledata.py

@time: 2017/11/4 下午2:40

@desc:
'''

from bestat.utils import get_neighbor
from bestat.models import Neighbor
import pickle
from tqdm import tqdm
from glob import glob

files = glob('./bestat/data/crime/crime_*.pkl')
for fi in tqdm(files):
    city = ' '.join(fi.split('_')[-1].split('.')[0].split('+'))
    print(city)
    with open(fi, 'rb') as f:
        data = pickle.load(f)

    nbs = Neighbor.objects.filter(city__exact=city)
    print(len(nbs))
    #
    # for key in data:
    #     records = data[key]
    #     for id in tqdm(records):
    #         r = records[id]
    #         lat = r['lat']
    #         lng = r['lon']
    #         nb = get_neighbor(lat, lng)
    #         if nb and nb.city == city:
    #             setattr(nb.crimes, key, getattr(nb.crimes, key) + 1)
    #             nb.crimes.save()
