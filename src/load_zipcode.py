# encoding: utf-8

'''

@author: ZiqiLiu


@file: load_zipcode.py

@time: 2017/11/29 上午2:19

@desc:
'''

from bestat.models import ZipcodeInfo
import json
from tqdm import tqdm
with open('./bestat/data/zipcode_info','r') as f:
    data = json.load(f)
for code in tqdm(data):
    info = data[code]
    zipcodeinfo = ZipcodeInfo(code=code)
    for k in info:
        setattr(zipcodeinfo, k, info[k])
    zipcodeinfo.save()
