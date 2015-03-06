from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User
from api.constants import SUBSCRIPTION_STATUS, SUBSCRIPTION_UNWATCHED


class Season(models.Model):
    season_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    cover = models.URLField(blank=True)
    default = models.BooleanField(default=False)


class Anime(models.Model):
    aid = models.TextField(default=0)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_end = models.BooleanField(default=False)
    episode = models.IntegerField(default=0)
    link = models.URLField(blank=True)
    season = models.ForeignKey(Season, related_name='anime')
    poster_link = models.CharField(max_length=300, default='')
    updated_time = models.DateTimeField(default=timezone.now())
    subscription = models.ManyToManyField(User, through='Subscription')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-updated_time']


class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='user')
    anime = models.ForeignKey(Anime, related_name='anime')
    is_read = models.BooleanField(default=False)
    currently_read = models.IntegerField(default=0)
    status = models.IntegerField(default=SUBSCRIPTION_UNWATCHED, choices=SUBSCRIPTION_STATUS)

    def __unicode__(self):
        return self.anime.name

