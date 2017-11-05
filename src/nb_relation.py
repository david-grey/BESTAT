# encoding: utf-8

'''

@author: ZiqiLiu


@file: nb_relation.py

@time: 2017/11/5 下午6:00

@desc:
'''
import csv
from bestat.models import Neighbor, PLACES_TYPE
from tqdm import tqdm

with open('./bestat/data/nrelation.csv', 'r') as f:
    reader = csv.reader(f, delimiter=",")
    data = [(line[1], line[3]) for line in reader]
graph = {}

for source, adj in data:
    if source in graph:
        graph[source].append(adj)
    else:
        graph[source] = [adj]

prefix = 'nb_'
for source in tqdm(graph):
    try:
        nb = Neighbor.objects.get(id=source)
        adj_resource = {}
        for tp in PLACES_TYPE:
            adj_resource[tp] = 0

        for adj_id in graph[source]:
            adj_nb = Neighbor.objects.get(id=adj_id)
            for tp in adj_resource:
                adj_resource[tp] += getattr(adj_nb, tp, 0)

        for tp in adj_resource:
            setattr(nb, prefix + tp, adj_resource[tp])

    except Neighbor.DoesNotExist:
        pass
