# encoding: utf-8

'''

@author: ZiqiLiu


@file: factfinder.py

@time: 2017/10/8 下午8:54

@desc:
'''
import requests
from bs4 import BeautifulSoup
import json
from multiprocessing import Pool

ITEMS = {'POPULATION': None, 'AGE': None, 'EDUCATION': None, 'HOUSING': None,
         'INCOME': None, 'POVERTY': None}

BASE_URL = 'https://factfinder.census.gov/rest/communityFactsNav/nav?N=0&searchTerm={}&spotlightId={}&log=t'


def parse(s):
    if '%' in s:
        return eval(s[:-2]) / 100
    if ',' in s:
        return eval(s.replace(',', ''))
    return eval(s)


def fetch(zip_code):
    """
    
    :param zip_code: 
    :return: dict
    """
    result = {}

    for item in ITEMS:
        try:
            content = \
                requests.get(BASE_URL.format(zip_code, item)).json()[
                    'CFMetaData'][
                    'measureAndLinksContent']
            # print(requests.get(BASE_URL.format(zip_code, item)).url)
            if '<h2>United States</h2>' in content:
                # print(content)
                # print(content)
                print('invalid zipcode')
                return None

            soup = BeautifulSoup(content, 'lxml')

            result[item] = parse(soup.find(name='div', class_='value').text)
        except AttributeError:
            print('missing field')
            return None
    print(result)
    return result


def fetch_all(codes, n):
    results = {}
    for i in codes:
        code = str(i).zfill(5)
        print('zipcode', code)
        res = fetch(code)
        if res:
            results[i] = res
        if int(i) % 5000 == 0:
            with open('./zipcode_info{}_{}'.format(n,i), 'w') as f:
                json.dump(results, f)
    with open('./zipcode_info', 'w') as f:
        json.dump(results, f)



def div_list(li, n):
    length = len(li)
    t = length // n
    quaters = [t * i for i in range(0, n)]

    result = [li[quaters[i]:quaters[i + 1]] for i in range(0, n - 1)]
    result.append(li[quaters[n - 1]:len(li)])
    return result


def multi():
    process_num = 8

    codes = [str(i).zfill(5) for i in range(99999)]
    lists = div_list(codes, process_num)
    print('started')
    # fetch_all(lists[0],1)

    p = Pool()

    for i in range(process_num):
        p.apply_async(fetch_all, args=(lists[i], i))
    p.close()
    p.join()
    print('finished')


if __name__ == '__main__':
    fetch_all([str(i).zfill(5) for i in range(0, 99999)], 1)
    # multi()
    # fetch('71646')
