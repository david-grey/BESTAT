# encoding: utf-8

'''

@author: ZiqiLiu


@file: utils.py

@time: 2017/10/25 下午2:55

@desc:
'''

from bestat.models import Neighbor, NeighborInfo


def is_anonymous(request):
    return request.user.is_anonymous


def get_neighbor(lat, lng):
    '''
    
    :param lat: 
    :param lng: 
    :return: return Neighbor object given the lat and lng of single point
    '''
    pnt_wkt = 'POINT(%f %f)' % (lng, lat)
    set = Neighbor.objects.filter(geom__contains=pnt_wkt)
    return set[0] if len(set) > 0 else None
