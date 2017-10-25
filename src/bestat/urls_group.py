# encoding: utf-8

'''

@author: ZiqiLiu


@file: urls_group.py

@time: 2017/10/2 下午6:01

@desc:
'''
from django.conf.urls import url, include
import grumblr.views

blog_urls = [
    url(r'^create_blog$', grumblr.views.create_blog, name='create_blog'),
    url(r'^delete/(?P<blog_id>[0-9]+)$', grumblr.views.delete_blog,
        name='delete_blog'),
    url(r'^get_update/$', grumblr.views.update_blogs),
    url(r'^add_comment/$', grumblr.views.add_comment),
    url(r'^delete_comment/$', grumblr.views.delete_comment),
    url(r'^likes/(?P<blog_id>[0-9]+)$', grumblr.views.likes),

]

profile_urls = [
    url(r'^$', grumblr.views.profile, name='profile'),
    url(r'^(?P<user_id>[^=]+)$', grumblr.views.profile, name='view_profile'),
    url(r'^follow=(?P<followee_id>[0-9]+)$', grumblr.views.follow,
        name='follow'),
    url(r'^unfollow=(?P<followee_id>[0-9]+)$', grumblr.views.unfollow,
        name='unfollow'),
]
