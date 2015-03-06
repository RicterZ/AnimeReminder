__author__ = 'Ricter'

from django.conf.urls import patterns, url, include
from rest_framework import routers
from api import views


router = routers.DefaultRouter()
router.register(r'anime', views.AnimeViewSet, base_name='anime')
router.register(r'subscriptions', views.SubscriptionViewSet, base_name='subscription')
router.register(r'search', views.SearchViewSet, base_name='search')
router.register(r'profile', views.UserViewSet, base_name='profile')


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)