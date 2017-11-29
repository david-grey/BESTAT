# encoding: utf-8

'''

@author: ZiqiLiu


@file: get_city_bound.py

@time: 2017/11/13 下午3:07

@desc:
'''

import json
import numpy as np
from bestat.models import Neighbor


def get_nb_bound(neighbor):
    points = np.asarray(json.loads(neighbor.geom.json)['coordinates'][0][0])
    northeast = np.max(points, 0)
    southwest = np.min(points, 0)
    return northeast, southwest


def get_city_bound(city_name):
    ne = []
    sw = []
    nbs = Neighbor.objects.filter(city=city_name)
    for nb in nbs:
        northeast, southwest = get_nb_bound(nb)
        ne.append(northeast)
        sw.append(southwest)
    ne = np.asarray(ne)
    sw = np.asarray(sw)
    ne = np.max(ne, 0)
    sw = np.min(sw, 0)

    return ne[1], sw[1], sw[0], ne[0]


def get_all_city_bound():
    cities = [nb.city for nb in Neighbor.objects.all().distinct('city')]
    bounds = [get_city_bound(c) for c in cities]
    return bounds
