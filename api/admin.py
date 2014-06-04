from django.contrib import admin
from api.models import Group, Anime, Subscription, UserExtension

admin.site.register(Group)
admin.site.register(Anime)
admin.site.register(Subscription)
admin.site.register(UserExtension)