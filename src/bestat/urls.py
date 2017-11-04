# encoding: utf-8

'''

@author: ZiqiLiu


@file: urls.py

@time: 2017/10/2 下午6:01

@desc:
'''

from django.conf.urls import url, include
import bestat.views

urlpatterns = [
    url(r'^$', bestat.views.home),
    url(r'^signup/?$', bestat.views.signup, name='signup'),
    url(r'^signin/?$', bestat.views.signin, name='signin'),
    url(r'^logout/?$', bestat.views.logout_user, name='logout'),
    url(r'^confirm/username=(?P<username>[0-9a-zA-Z]+)&token=(?P<token>\S+)$',
        bestat.views.confirm, name='confirm'),
    url(r'^map/$', bestat.views.get_city, name='map'),
    url(r'^load_city/(?P<city>[a-zA-Z]+)$', bestat.views.load_city, name='load_city'),
]

