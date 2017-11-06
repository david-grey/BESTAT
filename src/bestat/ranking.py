# encoding: utf-8

'''

@author: ZiqiLiu


@file: ranking.py

@time: 2017/11/4 下午10:04

@desc:
'''
import numpy as np
from bestat.models import Neighbor, NeighborInfo

CRIME_WEIGHT = 4.

# 80 tile and 20 tile
NTILE = {'hospital': (2, 0), 'store': (47, 10), 'cafe': (3, 0),
         'church': (7, 1), 'school': (7, 1), 'grocery_or_supermarket': (2, 0),
         'bank': (2, 0), 'gym': (2, 0), 'restaurant': (15, 4),
         'subway_station': (2, 0)}

CRIME_SCORES = {'Theft': 2, 'Robbery': 3, 'Burglary': 3,
                'Vandalism': 2, 'Shooting': 5, 'Arson': 4, 'Arrest': 4,
                'Assault': 4, 'Other': 1}

PUBLIC_SERVICE_ITEM = {'hospital', 'church', 'school'}
LIVE_CONVENIENCE_ITEM = {'store', 'cafe', 'bank', 'restaurant',
                         'grocery_or_supermarket', 'gym'}

CRIME_NTILE80 = 200
CRIME_NTILE20 = 20

ADJ_PREFIX = 'nb_'
ADJ_WEIGHT = .3


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
    public_service = 0  # hospital, school, church
    live_convenience = 0  # store, cafe, gym, bank, restaurant, grocery_or_supermarket
    for key in NTILE:

        # weighted avg with adjacent neighbor
        item_score = (1 - ADJ_WEIGHT) * get_item_score(key,
                                                       getattr(nb.info, key))
        item_score += ADJ_WEIGHT * get_item_score(key, getattr(nb.info,
                                                               ADJ_PREFIX + key))

        score += item_score
        public_service += item_score if key in PUBLIC_SERVICE_ITEM else 0
        live_convenience += item_score if key in LIVE_CONVENIENCE_ITEM else 0
    crime_index = 0
    for key in CRIME_SCORES:
        crime_index += getattr(nb.crimes, key) * CRIME_SCORES[key]
    scaled_crime_index = my_sigmoid(crime_index, (CRIME_NTILE80, CRIME_NTILE20))
    overall = score - scaled_crime_index * CRIME_WEIGHT

    # adjust for overall score
    overall += 2
    overall = min(10., overall)

    # adjust for public service
    public_service = public_service / 3 * 10

    # adjust for live convenience
    live_convenience = live_convenience / 6 * 10

    # adjust for crime
    security_score = (1 - scaled_crime_index) * 10

    return overall, public_service, live_convenience, security_score
