# encoding: utf-8

'''

@author: ZiqiLiu


@file: urls.py

@time: 2017/10/2 下午6:01

@desc:
'''

from django.conf.urls import url, include
import bestat.views
from django.views.static import serve
import webapps.settings as settings

urlpatterns = [
    url(r'^$', bestat.views.home, name='home'),
    url(r'^signup/?$', bestat.views.signup, name='signup'),
    url(r'^signin/?$', bestat.views.signin, name='signin'),
    url(r'^logout/?$', bestat.views.logout_user, name='logout'),
    url(r'^confirm/username=(?P<username>[0-9a-zA-Z]+)&token=(?P<token>\S+)$',
        bestat.views.confirm, name='confirm'),
    url(r'^detail/(?P<neighbor_id>[0-9]+)$', bestat.views.detail,
        name='detail'),
    url(r'^map/$', bestat.views.get_city, name='city'),
    url(r'^get_all_city/$', bestat.views.get_all_city, name='get_all_city'),
    url(r'^load_city/(?P<city>[a-zA-z\s]+)$', bestat.views.load_city,
        name='load_city'),
    url(r'^get_neighbor_detail/(?P<neighbor_id>[0-9]+)$',
        bestat.views.get_neighbor_detail, name='get_neighbor_detail'),
    url(r'^get_review_detail/(?P<neighbor_id>[0-9]+)$',
        bestat.views.get_review_detail, name='get_review_detail'),
    url(r'^get_reviews/(?P<neighbor_id>[0-9]+)$', bestat.views.get_reviews,
        name='get_reviews'),
    url(r'^create_review$', bestat.views.create_review, name='create_review'),
    url(r'^get_picture/$', bestat.views.get_picture, name='get_picture'),
    url(r'^edit_profile/$', bestat.views.edit_profile, name='edit_profile'),
    url(r'^change_password/$', bestat.views.change_password,
        name='change_password'),
    url(r'^preference/$', bestat.views.preference, name='preference'),
    url(r'^cities/$', bestat.views.cities, name='cities'),
    url(r'^neighbors/$', bestat.views.neighbors, name='neighbors'),
    url(r'get_city_picture/$', bestat.views.get_city_pic, name="get_city_picture"),
    url(r'^forget_password/?$', bestat.views.forget_password,
        name='forget_password'),
    url(r'^reset/username=(?P<user_id>[0-9a-zA-Z]+)&token=(?P<token>\S+)$',
        bestat.views.reset_password_check, name='reset'),
    url(r'^reset_password/$', bestat.views.reset_password,
        name='reset_password')

]

urlpatterns+= [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ]