# encoding: utf-8

'''

@author: ZiqiLiu


@file: clean_city.py

@time: 2017/11/4 下午9:50

@desc:
'''

from bestat.models import NeighborInfo, Neighbor
from tqdm import tqdm

attrs = ['church', 'hospital', 'restaurant', 'gym', 'cafe', 'bank', 'store',
         'grocery_or_supermarket', 'subway_station', 'school']
nbs = Neighbor.objects.filter(city='Chicago')
for nb in tqdm(nbs):
    for attr in attrs:
        setattr(nb.info, attr, 0)
        nb.info.save()
