from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User
from api.constants import SUBSCRIPTION_STATUS, SUBSCRIPTION_UNWATCHED, BANGUMI_END_STATUS, BANGUMI_NOT_END



class Anime(models.Model):
    aid = models.TextField(default=0)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_end = models.IntegerField(choices=BANGUMI_END_STATUS, default=BANGUMI_NOT_END)
    episode = models.IntegerField(default=0)
    link = models.URLField(blank=True)
    poster_link = models.CharField(max_length=300, default='')
    updated_time = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-updated_time']


class Season(models.Model):
    season_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    cover = models.URLField(blank=True)
    default = models.BooleanField(default=False)
    anime = models.ForeignKey(Anime, related_name='seasons')
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s %s' % (self.anime, self.name)


class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='user')
    anime = models.ForeignKey(Anime, related_name='anime')
    season = models.OneToOneField(Season, related_name='season', null=True, blank=True)
    currently_read = models.IntegerField(default=0)
    status = models.IntegerField(default=SUBSCRIPTION_UNWATCHED, choices=SUBSCRIPTION_STATUS)

    def __unicode__(self):
        return '%s: %s' % (self.user.username, self.anime.name)
