# encoding: utf-8

'''

@author: ZiqiLiu


@file: models.py

@time: 2017/10/11 下午7:12

@desc:
'''
from django.contrib.auth.models import User
from django.db import models


class Block(models.Model):
    id = models.CharField(max_length=64, verbose_name='block_id',
                          primary_key=True)

    # attrs from factfinder, base on zipcode
    population = models.IntegerField(null=True, blank=True)
    age = models.FloatField(null=True, blank=True)
    # Educational Attainment: Percent high school graduate or higher
    education = models.FloatField(null=True, blank=True)
    housing = models.IntegerField(null=True, blank=True)
    income = models.IntegerField(null=True, blank=True)
    # % Individuals below poverty level
    poverty = models.FloatField(null=True, blank=True)


class CrimeRecord(models.Model):
    block = models.OneToOneField(Block, related_name='crimes',
                                 on_delete=models.CASCADE,
                                 primary_key=True, )
    Theft = models.IntegerField(null=True, blank=True)
    Robbery = models.IntegerField(null=True, blank=True)
    Burglary = models.IntegerField(null=True, blank=True)
    Vandalism = models.IntegerField(null=True, blank=True)
    Shooting = models.IntegerField(null=True, blank=True)
    Arson = models.IntegerField(null=True, blank=True)
    Arrest = models.IntegerField(null=True, blank=True)
    Assault = models.IntegerField(null=True, blank=True)
    Other = models.IntegerField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scores = {'Theft': 2, 'Robbery': 3, 'Burglary': 3,
                       'Vandalism': 2, 'Shooting': 5, 'Arson': 4, 'Arrest': 4,
                       'Assault': 4, 'Other': 1}


class BlockPlaces(models.Model):
    block = models.OneToOneField(Block, related_name='places',
                                 on_delete=models.CASCADE,
                                 primary_key=True, )

    restaurant = models.IntegerField(null=True, blank=True)
    shopping = models.IntegerField(null=True, blank=True)
    store = models.IntegerField(null=True, blank=True)
    education = models.IntegerField(null=True, blank=True)
    medical = models.IntegerField(null=True, blank=True)
    transportation = models.IntegerField(null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile',
                                on_delete=models.CASCADE,
                                primary_key=True, )
    nick_name = models.CharField(max_length=64, verbose_name='nick name')
    gender = models.CharField(max_length=10,
                              choices=(('male', 'male'), ('female', 'female')))
    img = models.ImageField(upload_to='', default='user_default.png')
    favorites = models.ManyToManyField(Block, related_name='prefer_users')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reviews')
    text = models.TextField()
    create_time = models.DateTimeField(verbose_name='create time',
                                       auto_now_add=True)
