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
    url(r'^$', bestat.views.home, name='home'),
    url(r'^signup/?$', bestat.views.signup, name='signup'),
    url(r'^signin/?$', bestat.views.signin, name='signin'),
    url(r'^logout/?$', bestat.views.logout_user, name='logout'),
    url(r'^confirm/username=(?P<username>[0-9a-zA-Z]+)&token=(?P<token>\S+)$',
        bestat.views.confirm, name='confirm'),
    url(r'^detail/$', bestat.views.detail, name='detail'),
    url(r'^map/$', bestat.views.get_city, name='city'),
    url(r'^get_all_city/$', bestat.views.get_all_city, name='get_all_city'),
    url(r'^load_city/(?P<city>[a-zA-Z]+)$', bestat.views.load_city,
        name='load_city'),

]