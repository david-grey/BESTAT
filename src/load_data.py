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
    for key_record in records:
        r = records[key_record]
        lat = r['lat']
        lng = r['lng']
        nb = get_neighbor(lat, lng)
        nb.info.objects.update_or_create(population=111)

from bestat.models import Neighbor,NeighborInfo
from tqdm import tqdm
allnbs = Neighbor.objects.all()
for nb in tqdm(allnbs):
    inf = NeighborInfo(neighbor=nb)
    inf.save()
