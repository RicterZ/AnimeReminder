from django.contrib import admin
from api.models import Anime, Subscription, Season, Track


admin.site.register(Anime)
admin.site.register(Season)
admin.site.register(Subscription)
admin.site.register(Track)