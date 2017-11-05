# encoding: utf-8

'''

@author: ZiqiLiu


@file: circle.py

@time: 2017/10/31 下午7:36

@desc: as all data api is circle-based, 
we will store those data as circle-based into database.
In order to leverage PostGIS, which store region info as polygon,
we use octagon to approximate circle
'''

import math
import numpy as np

default_radius = 400.
# pittsburgh west to east roughly: -80.033, -79.903
# pittsburgh south to north roughly: 40.387, 40.507
sqrt2 = math.sqrt(2)
EARTH_RADIU = 6371393


def distance2degree(d):
    return d / EARTH_RADIU * 180 / math.pi


DISTANCE_BETWEEN_CENTER = distance2degree(default_radius) * sqrt2 * 0.95


def octagon(center, r=default_radius):
    '''
    
    :param center: (x,y)
    :param r: float
    :return: 8 points of (x,y)
    '''
    x = center[0]
    y = center[1]
    return ((x, y + r), (x + r / sqrt2, y + r / sqrt2), (x + r, y),
            (x + r / sqrt2, y - r / sqrt2), (x, y - r),
            (x - r / sqrt2, y - r / sqrt2), (x - r, y),
            (x - r / sqrt2, y + r / sqrt2))


def get_circles(up, down, left, right,radius=DISTANCE_BETWEEN_CENTER):
    '''
    
    :param up: 
    :param down: 
    :param left: 
    :param right: 
    :return: list of points of (lat, lng)
    '''
    lat_range = np.arange(down, up, radius)
    lng_range = np.arange(left, right, radius)
    points = []
    for lat in lat_range:
        for lng in lng_range:
            points.append((lat, lng))

    return points


# return list of circle, given a bounding box

