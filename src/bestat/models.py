# encoding: utf-8

'''

@author: ZiqiLiu


@file: models.py

@time: 2017/10/11 下午7:12

@desc:
'''
from django.contrib.auth.models import User
from django.contrib.gis.db import models
import datetime
from django.db.models.aggregates import Max

PLACES_TYPE = {'hospital', 'restaurant', 'store', 'bank', 'school',
               'subway_station', 'church', 'cafe', 'gym',
               'grocery_or_supermarket'}


# ['doctor', 'restaurant', 'store', 'bank', 'school', 'subway_station', 'church', 'cafe', 'gym', 'grocery_or_supermarket']

class Neighbor(models.Model):
    state = models.CharField(max_length=80)
    county = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    regionid = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)


class NeighborInfo(models.Model):
    neighbor = models.OneToOneField(Neighbor, on_delete=models.CASCADE,
                                    related_name="info", primary_key=True)

    # attrs from factfinder, base on zipcode
    population = models.IntegerField(null=True, blank=True)
    age = models.FloatField(null=True, blank=True)
    # Educational Attainment: Percent high school graduate or higher
    education = models.FloatField(null=True, blank=True)
    housing = models.IntegerField(null=True, blank=True)
    income = models.IntegerField(null=True, blank=True)
    # % Individuals below poverty level
    poverty = models.FloatField(null=True, blank=True)

    # liked = models.ManyToManyField(Profile, related_name='favorite_nb')

    # ['doctor', 'restaurant', 'store', 'bank', 'school', 'subway_station', 'church', 'cafe', 'gym', 'grocery_or_supermarket']
    hospital = models.IntegerField(default=0)
    restaurant = models.IntegerField(default=0)
    store = models.IntegerField(default=0)
    bank = models.IntegerField(default=0)
    school = models.IntegerField(default=0)
    subway_station = models.IntegerField(default=0)
    church = models.IntegerField(default=0)
    cafe = models.IntegerField(default=0)
    gym = models.IntegerField(default=0)
    grocery_or_supermarket = models.IntegerField(default=0)

    nb_hospital = models.IntegerField(default=0)
    nb_restaurant = models.IntegerField(default=0)
    nb_store = models.IntegerField(default=0)
    nb_bank = models.IntegerField(default=0)
    nb_school = models.IntegerField(default=0)
    nb_subway_station = models.IntegerField(default=0)
    nb_church = models.IntegerField(default=0)
    nb_cafe = models.IntegerField(default=0)
    nb_gym = models.IntegerField(default=0)
    nb_grocery_or_supermarket = models.IntegerField(default=0)

    @property
    def likes_num(self):
        return self.liked_users.count()


CRIME_SCORES = {'Theft': 2, 'Robbery': 3, 'Burglary': 3,
                'Vandalism': 2, 'Shooting': 5, 'Arson': 4, 'Arrest': 4,
                'Assault': 4, 'Other': 1}


class CrimeRecord(models.Model):
    neighbor = models.OneToOneField(Neighbor, related_name='crimes',
                                    on_delete=models.CASCADE,
                                    primary_key=True, )
    Theft = models.IntegerField(default=0)
    Robbery = models.IntegerField(default=0)
    Burglary = models.IntegerField(default=0)
    Vandalism = models.IntegerField(default=0)
    Shooting = models.IntegerField(default=0)
    Arson = models.IntegerField(default=0)
    Arrest = models.IntegerField(default=0)
    Assault = models.IntegerField(default=0)
    Other = models.IntegerField(default=0)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile',
                                on_delete=models.CASCADE,
                                primary_key=True, )
    nick_name = models.CharField(max_length=64, verbose_name='nick name')
    img = models.ImageField(upload_to='', default='user_default.png')
    favorites = models.ManyToManyField(NeighborInfo, related_name='liked_users')


class Preference(models.Model):
    user = models.OneToOneField(User, related_name='preference',
                                on_delete=models.CASCADE,
                                primary_key=True, )
    hospital = models.FloatField(default=5.)
    restaurant = models.FloatField(default=5.)
    store = models.FloatField(default=5.)
    bank = models.FloatField(default=5.)
    school = models.FloatField(default=5.)
    church = models.FloatField(default=5.)
    cafe = models.FloatField(default=5.)
    gym = models.FloatField(default=5.)
    grocery_or_supermarket = models.FloatField(default=5.)
    crime = models.FloatField(default=5.)


class Review(models.Model):
    block = models.ForeignKey(NeighborInfo, on_delete=models.CASCADE,
                              related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    text = models.TextField()
    safety = models.IntegerField()
    convenience = models.IntegerField()
    public_service = models.IntegerField()
    create_time = models.DateTimeField(verbose_name='create time',
                                       auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes',
                                   related_query_name='like')

    @property
    def likes_num(self):
        return self.likes.all().count()

    @property
    def create_at(self):
        return self.create_time.timestamp()

    @staticmethod
    def get_max_time():
        return int((Review.objects.all().aggregate(Max('create_time'))[
                        'create_time__max'] or datetime.datetime.now()).timestamp())


# Auto-generated `LayerMapping` dictionary for Neighbor model
neighbor_mapping = {
    'state': 'State',
    'county': 'County',
    'city': 'City',
    'name': 'Name',
    'regionid': 'RegionID',
    'geom': 'MULTIPOLYGON',
}


class City(models.Model):
    name = models.CharField(max_length=255)
    point = models.PointField(srid=4326)
    activate = models.IntegerField(default=0)
    population = models.IntegerField()


class Zipcode(models.Model):
    zcta5ce10 = models.CharField(max_length=5)
    geoid10 = models.CharField(max_length=5)
    classfp10 = models.CharField(max_length=2)
    mtfcc10 = models.CharField(max_length=5)
    funcstat10 = models.CharField(max_length=1)
    aland10 = models.BigIntegerField()
    awater10 = models.BigIntegerField()
    intptlat10 = models.CharField(max_length=11)
    intptlon10 = models.CharField(max_length=12)
    geom = models.MultiPolygonField(srid=4326)

# Auto-generated `LayerMapping` dictionary for Zipcode model

class ZipcodeInfo(models.Model):
    code = models.CharField(primary_key=True, max_length=5)
    income = models.IntegerField(null=True, blank=True)
    education = models.FloatField(null=True, blank=True)
    housing = models.IntegerField(null=True, blank=True)
    age = models.FloatField(null=True, blank=True)
    population = models.IntegerField(null=True, blank=True)
    poverty = models.FloatField(null=True, blank=True)

