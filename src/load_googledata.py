# encoding: utf-8

'''

@author: ZiqiLiu


@file: load_googledata.py

@time: 2017/11/4 下午2:40

@desc:
'''

from bestat.utils import get_neighbor, clean_nb_data
import pickle
from tqdm import tqdm
from glob import glob
from nb_relation import update_adj_nb


def file2city_name(file_name):
    city_name = ' '.join(file_name.split('_')[-1].split('.')[0].split('+'))
    return city_name


def load_data(pkl_name):
    city = file2city_name(pkl_name)
    clean_nb_data(city)
    print('loading data of city %s...' % city)
    with open('./bestat/data/googleplace/%s' % pkl_name, 'rb') as f:
        data = pickle.load(f)
    for key in data:
        records = data[key]
        for id in records:
            r = records[id]
            lat = r['lat']
            lng = r['lng']
            nb = get_neighbor(lat, lng)
            if nb and nb.city == city:
                setattr(nb.info, key, getattr(nb.info, key) + 1)
                nb.info.save()


def batch_load():
    pkls = map(lambda a: a.split('/')[-1],
               glob('./bestat/data/googleplace/googleplace_*.pkl'))
    print(pkls)
    for pkl in pkls:
        load_data(pkl)
        update_adj_nb(file2city_name(pkl))



if __name__ == '__main__':
    batch_load()
