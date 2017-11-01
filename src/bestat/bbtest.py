# encoding: utf-8

'''

@author: ZiqiLiu


@file: bbtest.py

@time: 2017/10/31 下午6:58

@desc:
'''

from bestat.MinimumBoundingBox import minimum_bounding_box

points = ((1, 4), (5, 4), (5, 1))
bounding_box = minimum_bounding_box(points)  # returns namedtuple

bounding_box.area  # 16
bounding_box.rectangle_center  # (1.3411764705882352, 1.0647058823529414)
print(
    bounding_box.corner_points)  # {(5, 4), (-1, -3), (-2.32, -1.87), (3.68, 5.13)}
