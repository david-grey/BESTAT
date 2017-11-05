# encoding: utf-8

'''

@author: ZiqiLiu


@file: ranking.py

@time: 2017/11/4 下午10:04

@desc:
'''
import numpy as np
from bestat.models import Neighbor, NeighborInfo

PUBLIC_SERVICES_WEIGHT = 1.
LIVE_CONVENIENCE_WEIGHT = 1.
CRIME_WEIGHT = 4.

# 80 tile and 20 tile
NTILE = {'hospital': (2, 0), 'store': (47, 10), 'cafe': (3, 0),
         'church': (7, 1), 'school': (7, 1), 'grocery_or_supermarket': (2, 0),
         'bank': (2, 0), 'gym': (2, 0), 'restaurant': (15, 4),
         'subway_station': (2, 0)}

CRIME_SCORES = {'Theft': 2, 'Robbery': 3, 'Burglary': 3,
                'Vandalism': 2, 'Shooting': 5, 'Arson': 4, 'Arrest': 4,
                'Assault': 4, 'Other': 1}

CRIME_NTILE80 = 200
CRIME_NTILE20 = 20


def my_sigmoid(x, tiles):
    # scale that ntile_80 map to 2 in origin sigmoid, ntile20 to -2
    ntile_80, ntile_20 = tiles
    scale = (ntile_80 - ntile_20) / 4
    shift = (ntile_80 + ntile_20) / 2
    scaled_x = (x - shift) / scale
    return 1 / (1 + np.exp(-scaled_x))


def get_item_score(name, val):
    return my_sigmoid(val, NTILE[name])


def get_neighbor_score(nb):
    score = 0
    for key in NTILE:
        score += get_item_score(key, getattr(nb.info, key))
    crime_index = 0
    for key in CRIME_SCORES:
        crime_index += getattr(nb.crimes, key) * CRIME_SCORES[key]
    scaled_crime_index = my_sigmoid(crime_index, (CRIME_NTILE80, CRIME_NTILE20))

    return score - scaled_crime_index * CRIME_WEIGHT,scaled_crime_index
