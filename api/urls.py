__author__ = 'Ricter'

from django.conf.urls import patterns, url, include
from rest_framework import routers
from api import views


router = routers.DefaultRouter()
router.register(r'anime', views.AnimeViewSet, base_name='anime')
router.register(r'users', views.UserViewSet, base_name='user')


urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       )