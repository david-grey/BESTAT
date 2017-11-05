# encoding: utf-8

'''

@author: ZiqiLiu


@file: decorator.py

@time: 2017/10/25 下午6:23

@desc:
'''
from django.shortcuts import render
import functools
from django.shortcuts import HttpResponse


# for debug purpose
def check_anonymous(func):
    def wrapper(*args, **kw):
        print('=' * 20)
        if args[0].user.is_anonymous:
            print('anonymous')
        else:
            print('already login')
        return func(*args, **kw)

    return wrapper


def login_required(text="you haven't login!"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            if args[0].user.is_anonymous:
                return render(args[0], 'signin_1.html',
                              {'errors': [text if text else None]})
            return func(*args, **kw)

        return wrapper

    return decorator


def anonymous_only(text="you've already login"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            if not args[0].user.is_anonymous:
                return render(args[0], 'blank.html', {'msg': text})
            return func(*args, **kw)

        return wrapper

    return decorator
