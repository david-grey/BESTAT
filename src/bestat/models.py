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
                                    related_name="nbinfo", primary_key=True)

    # attrs from factfinder, base on zipcode
    population = models.IntegerField(null=True, blank=True)
    age = models.FloatField(null=True, blank=True)
    # Educational Attainment: Percent high school graduate or higher
    education = models.FloatField(null=True, blank=True)
    housing = models.IntegerField(null=True, blank=True)
    income = models.IntegerField(null=True, blank=True)
    # % Individuals below poverty level
    poverty = models.FloatField(null=True, blank=True)

    # ['doctor', 'restaurant', 'store', 'bank', 'school', 'subway_station', 'church', 'cafe', 'gym', 'grocery_or_supermarket']
    doctor = models.IntegerField(default=0)
    restaurant = models.IntegerField(default=0)
    store = models.IntegerField(default=0)
    bank = models.IntegerField(default=0)
    school = models.IntegerField(default=0)
    subway_station = models.IntegerField(default=0)
    church = models.IntegerField(default=0)
    cafe = models.IntegerField(default=0)
    gym = models.IntegerField(default=0)
    grocery_or_supermarket = models.IntegerField(default=0)

    @property
    def likes_num(self):
        return self.liked_users.count()


class CrimeRecord(models.Model):
    block = models.OneToOneField(NeighborInfo, related_name='crimes',
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


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile',
                                on_delete=models.CASCADE,
                                primary_key=True, )
    nick_name = models.CharField(max_length=64, verbose_name='nick name')
    img = models.ImageField(upload_to='', default='user_default.png')
    favorites = models.ManyToManyField(NeighborInfo, related_name='liked_users')


class Review(models.Model):
    block = models.ForeignKey(NeighborInfo, on_delete=models.CASCADE,
                              related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    text = models.TextField()
    create_time = models.DateTimeField(verbose_name='create time',
                                       auto_now_add=True)

    @property
    def create_at(self):
        return self.create_time.timestamp()

    @staticmethod
    def get_changes(time, user=None, stream=False):
        '''

        :param time: 
        :param user: if specify, then return personal blog or personal streams
        :param stream: used with user
        :return: 
        '''

        time = datetime.datetime.fromtimestamp(time + 1)
        if user:
            if stream:
                followees = user.profile.followees.all()
                stream_blogs = []
                for f in followees:
                    stream_blogs.extend(
                        f.user.blogs.filter(create_time__gt=time))
                stream_blogs = sorted(stream_blogs,
                                      key=lambda blog: blog.id,
                                      reverse=True)
                return stream_blogs
            else:
                return Review.objects.filter(author=user,
                                             create_time__gt=time)
        else:
            # global stream
            return Review.objects.filter(create_time__gt=time)

    @staticmethod
    def get_max_time():
        return int((Review.objects.all().aggregate(Max('create_time'))[
                        'create_time__max'] or datetime.datetime.now()).timestamp())


# a review can have multiple comments
class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments',
                               related_query_name='comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments',
                               related_query_name='comment')
    text = models.CharField(max_length=140, verbose_name='text')
    create_time = models.DateTimeField(verbose_name='create time',
                                       auto_now_add=True)
    test = models.IntegerField()


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
    geometry = models.PointField()

