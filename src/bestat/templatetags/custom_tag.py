# encoding: utf-8

'''

@author: ZiqiLiu


@file: custom_tag.py

@time: 2017/10/13 下午7:55

@desc:
'''

from django import template

register = template.Library()


@register.simple_tag
def check_liked(blog, user):
    return blog.liked(user)


def own_blog(blog, user):
    return blog.author == user
