# encoding: utf-8

'''

@author: ZiqiLiu


@file: utils.py

@time: 2017/10/25 下午2:55

@desc:
'''

from bestat.models import Neighbor, NeighborInfo, PLACES_TYPE
from tqdm import tqdm


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


def clean_nb_data(city_name):
    '''
    
    :param city: 
    :return: clean place type and nb place type data
    '''
    print('cleaning data of city %s...' % city_name)
    nbs = Neighbor.objects.filter(city=city_name)
    for nb in tqdm(nbs):
        for key in PLACES_TYPE:
            setattr(nb.info, key, 0)
        nb.info.save()


def clean_adj_data(city_name):
    prefix = 'nb_'
    print('cleaning adj data of city %s...' % city_name)
    nbs = Neighbor.objects.filter(city=city_name)
    for nb in tqdm(nbs):
        for key in PLACES_TYPE:
            setattr(nb.info, prefix + key, 0)
        nb.info.save()


if __name__ == '__main__':
    pass
    # clean_nb_data('Pittsburgh')
