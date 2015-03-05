from django.contrib import admin
from api.models import Anime, Subscription, UserExtension


admin.site.register(Anime)
admin.site.register(Subscription)
admin.site.register(UserExtension)