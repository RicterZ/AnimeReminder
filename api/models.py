from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Anime(models.Model):
    aid = models.IntegerField(max_length=6)
    name = models.CharField(max_length=100)
    intro = models.TextField(blank=True)
    is_end = models.BooleanField(default=False)
    bilibili_link = models.URLField(blank=True)
    poster_link = models.CharField(max_length=60)
    updated_time = models.DateTimeField(default=timezone.now())
    user = models.ManyToManyField(through='Subscription')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-updated_date']


class Subscription(models.Model):
    anime = models.ForeignKey(Anime, related_name='subs')
    user = models.ForeignKey(User, related_name='users')
    is_read = models.BooleanField(default=False)
    currently_read = models.IntegerField(default=0)
