from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User
from api.constants import SUBSCRIPTION_STATUS, SUBSCRIPTION_UNWATCHED


class Anime(models.Model):
    aid = models.TextField(default='')
    name = models.CharField(max_length=100)
    intro = models.TextField(blank=True)
    is_end = models.BooleanField(default=False)
    episode = models.IntegerField(default=0)
    bilibili_aid = models.IntegerField(default=0)
    bilibili_name = models.CharField(max_length=100)
    bilibili_link = models.URLField(blank=True)
    bilibili_bgmcount = models.IntegerField(default=0)
    bilibili_season = models.IntegerField(default=1)
    poster_link = models.CharField(max_length=300, default='')
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
    status = models.IntegerField(default=SUBSCRIPTION_UNWATCHED, choices=SUBSCRIPTION_STATUS)

    def __unicode__(self):
        return self.anime.name


class UserExtension(User):
    user = models.OneToOneField(User)
    is_email_reminder = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    objects = UserManager()

    def __unicode__(self):
        return self.username