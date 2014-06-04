from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager
from .signals import *


class Group(models.Model):
    name = models.TextField(max_length=20)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class Anime(models.Model):
    aid = models.IntegerField(max_length=6, primary_key=True)
    name = models.CharField(max_length=100)
    intro = models.TextField(blank=True)
    is_end = models.BooleanField(default=False)
    episode = models.IntegerField(max_length=4, default=0)
    bilibili_aid = models.IntegerField(max_length=10, default=0)
    bilibili_name = models.CharField(max_length=100)
    bilibili_link = models.URLField(blank=True)
    bilibili_bgmcount = models.IntegerField(max_length=10, default=0)
    bilibili_season = models.IntegerField(max_length=10, default=1)
    poster_link = models.CharField(max_length=300)
    updated_time = models.DateTimeField(default=timezone.now())
    subscription = models.ManyToManyField(User, through='Subscription')

    def __unicode__(self):
        return self.name

    def get_episode_count(self):
        return self.episode if self.episode > self.bilibili_bgmcount else self.bilibili_bgmcount

    class Meta:
        ordering = ['-updated_time']


class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='user')
    anime = models.ForeignKey(Anime, related_name='anime')
    is_read = models.BooleanField(default=False)
    currently_read = models.IntegerField(default=0)
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return self.anime.name


class UserExtension(User):
    user = models.OneToOneField(User)
    is_email_reminder = models.BooleanField(default=False)

    objects = UserManager()