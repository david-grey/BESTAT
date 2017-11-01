import requests

import math

r = 6371393
d = 400
a = d / r * 180 / math.pi
# a=math.radians(0.004)
print(a)


def distance2radian(d):
    r = 6371393
    return d / r * 180 / math.pi
