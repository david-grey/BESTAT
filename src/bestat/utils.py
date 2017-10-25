# encoding: utf-8

'''

@author: ZiqiLiu


@file: utils.py

@time: 2017/10/25 下午2:55

@desc:
'''


def is_anonymous(request):
    return request.user.is_anonymous